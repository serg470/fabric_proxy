from lib.files import *
from lib.docker import *


@task()
def deploy():
    '''
    Deploy telegraf agent
    :return:
    '''
    # TODO: Change to connecting to artifacts repo at some point
    docker_login()
    docker_tag("docker.aaa.bbb.ccc/telegraf:latest", 'current')
    put_file("usr", "docker", "bin", "telegraf.sh", mode=0755)


@task()
def configure():
    '''
    Configure telegraf
    :return:
    '''
    put_file("usr", "docker", "conf", "telegraf", "telegraf.conf")
    put_file("etc", "supervisor", "conf.d", "telegraf.conf")
#    host = run('hostname')
#    sudo("sed -i -e 's/\!HOSTNAME\!/%s/g' /usr/docker/conf/telegraf/telegraf.conf" % str(host))
    run("supervisorctl update telegraf")
    pass


@task
def install():
    '''
    Deploys & configures telegraf
    :return:
    '''
    deploy()
    configure()
