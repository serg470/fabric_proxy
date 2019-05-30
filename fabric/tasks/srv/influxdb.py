from lib.files import *
from lib.docker import *


@task()
def deploy():
    '''
    Deploy influxdb agent
    :return:
    '''
    # TODO: Change to connecting to artifacts repo at some point
    put_file("usr", "docker", "bin", "influxdb.sh", mode=0755)
    sudo("mkdir -p /var/lib/influxdb")


@task()
def configure():
    '''
    Configure influxdb
    :return:
    '''
    put_file("usr", "docker", "conf", "influxdb", "influxdb.conf")
    put_file("etc", "supervisor", "conf.d", "influxdb.conf")
    run("supervisorctl update influxdb")
    pass


@task
def install():
    '''
    Deploys & configures influxdb
    :return:
    '''
    deploy()
    configure()
