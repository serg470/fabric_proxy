from getpass import getpass

from lib.docker import *
from lib.files import *


@task()
def deploy():
    """
    Deploy postgres

    :return:
    """
    # Check if secret exists
    if not exists("/dev/mapper/secret", use_sudo=True):
        raise Exception("Secret volume is not mounted")
    if not exists("/secret/postgres/postgres.passwd", use_sudo=True):
        passwd = getpass("Enter postgres password:")
        sudo("mkdir -p /secret/postgres")
        put(StringIO.StringIO(passwd), "/secret/postgres/postgres.passwd", mode=644, use_sudo=True)
    sudo("mkdir -p /var/docker/posgres/data /striped/data/postgres/archive /striped/logs/postgres")
    put_file("usr", "docker", "bin", "postgres.sh", mode=0755)


@task
def config_master(master, slave):
    """
    Config PostgreSQL master, create backup and dump, start replication

    :param master: server_name
    :param slave:  server_name
    :return:
    """
    # sudo("supervisorctl stop postgres && /bin/true")
    # sudo("docker stop postgres && /bin/true")
    configure()
    masterIp = run("host %s-vpn.locahlost | cut -d' ' -f4" % master)
    slaveIp = run("host %s-vpn.locahlost | cut -d' ' -f4" % slave)
    sudo("sed -i -e 's,slave,%s,g' /usr/docker/conf/postgres/postgresql_master.conf" % slave)
    sudo("sed -i -e 's,slaveIP,%s/32,g' /usr/docker/conf/postgres/pg_hba.conf" % slaveIp)
    sudo("sed -i -e 's,masterIP,%s/32,g' /usr/docker/conf/postgres/pg_hba.conf" % masterIp)
    sudo("mv -f /usr/docker/conf/postgres/postgresql_master.conf /usr/docker/conf/postgres/postgresql.conf")
    run("docker exec -i postgres psql -U postgres -c 'SELECT pg_reload_conf();'")
    #    manual_backup()
    pwd = run("date +%YYmD | md5sum | cut -d' ' -f1")
    run("export PASS='%s'" % pwd)
    run(
        "docker exec -i postgres psql -U postgres -c 'DROP USER IF EXISTS replica;'")
    run(
        "docker exec -i postgres psql -U postgres -c \"CREATE USER replica REPLICATION LOGIN ENCRYPTED PASSWORD '%s';\"" % pwd)
    sudo("mkdir -p /var/docker/posgres/data/archive")
    sudo("chmod 775 /var/docker/posgres/data/archive")
    # run("docker exec -i postgres pg_basebackup -h %s.locahlost -U replica -Ft -R -z -v -P -D /tmp/base" % master)
    run("docker exec -i postgres psql -U postgres -c \"SELECT pg_start_backup('backup');\"")
    sudo("tar czvf /tmp/startbackup.tar.gz -C /var/docker/posgres/data/ .")
    run("docker exec -i postgres psql -U postgres -c \"SELECT pg_stop_backup();\"")
    sudo("mv /usr/docker/conf/postgres/recovery.template /tmp")
    run("sed -i -e 's/slave/%s-vpn.locahlost/g' /tmp/recovery.template" % slave)
    run("sed -i -e 's/master/%s-vpn.locahlost/g' /tmp/recovery.template" % master)
    run("sed -i -e 's/PWD/%s/g' /tmp/recovery.template" % pwd)
    sudo("chmod 644 /tmp/startbackup.tar.gz")
    run("scp /tmp/startbackup.tar.gz %s.locahlost:/tmp/startbackup.tar.gz" % slave)
    run("scp /tmp/recovery.template %s.locahlost:/tmp/recovery.conf" % slave)


# TODO !!! Stop backup after move
# run("docker cp postgres:/tmp/base/base.tar /tmp/")
# run("gzip -9 /tmp/base.tar")
#    run("scp /tmp/base.tar.gz %s.locahlost:/tmp/startbackup.tar.gz" % slave)


#    sudo("supervisorctl restart postgres")


@task()
def manual_backup():
    """
    Manual full backup with autorotate and remote copy to i01. Please add -A options in fabric run command
    This backup dump only with schema web

    :return:
    """
    FREE = run('df /striped --output=pcent | tail -n -1 | cut -d% -f1')
    if FREE < "95":
        DATE = run("date +%u")
        if not exists("/striped/tmp"):
            sudo("mkdir -p /striped/tmp")
            user = whoami()
            sudo("chown %s /striped/tmp" % user)
        host = run("hostname")
        target = "/striped/tmp/full." + str(host) + "." + str(DATE).strip() + ".sql"
        run("docker exec postgres pg_dump \
                      -U database \
                      --quote-all-identifiers \
                      --if-exists \
                      --clean \
                      --schema='web' \
                      database > %s" % target)
        run("gzip -5 -f %s" % target)
        run("chmod 664 %s.gz" % target)
        run("scp -o StrictHostKeyChecking=no %s.gz i01.locahlost:/var/backups/postgres" % target)
        print(
                "The postgreSQL backup task has been completed. "
                "Local dump copy located at %s.gz, remote copy at i01:" % target)
    else:
        print("Check free space, the backup cann't be executed")


@task()
def config_slave(master, slave):
    """
    Config PostgreSQL slave, create backup and dump, get configuration, start replication

    :param master:
    :param slave:
    :return:
    """
    deploy()
    put_files("usr", "docker", "conf", "postgres", "*")
    put_file("etc", "supervisor", "conf.d", "postgres.conf")
    configure()
    masterIP = run("host %s-vpn.locahlost | cut -d' ' -f4" % master)
    slaveIP = run("host %s-vpn.locahlost | cut -d' ' -f4" % slave)
    sudo("sed -i -e 's/slave/%s/g' /usr/docker/conf/postgres/postgresql_slave.conf" % slave)
    sudo("sed -i -e 's,slaveIP,%s/32,g' /usr/docker/conf/postgres/pg_hba.conf" % slaveIP)
    sudo("sed -i -e 's,masterIP,%s/32,g' /usr/docker/conf/postgres/pg_hba.conf" % masterIP)
    sudo("supervisorctl restart postgres && sleep 15")
    sudo("supervisorctl stop postgres")
    sudo("mkdir -p /var/docker/posgres/data")
    sudo("cd /var/docker/posgres/data && tar xzpvf /tmp/startbackup.tar.gz")
    sudo("mv -f /usr/docker/conf/postgres/postgresql_slave.conf /usr/docker/conf/postgres/postgresql.conf")
    sudo("mv /tmp/recovery.conf /var/docker/posgres/data/")
    sudo("supervisorctl restart postgres && sleep 35")
    #    run("zcat /tmp/startbackup.tar.gz | docker exec -i postgres psql -U postgres")


# TODO STOP pg_base_backup on MASTER with 'SELECT pg_stop_backup()':

@task()
def configure():
    """
    Configure postgres

    :return:
    """
    put_files("usr", "docker", "conf", "postgres", "*")
    put_file("etc", "supervisor", "conf.d", "postgres.conf")
    sudo("supervisorctl update postgres")
    pass


@task()
def install():
    """
    Deploy & configure postgres

    :return:
    """
    deploy()
    configure()
