from lib.files import *
from lib.docker import *


@task()
def deploy():
    '''
    Deploy grafana agent
    :return:
    '''
    # TODO: Change to connecting to artifacts repo at some point
    put_file("usr", "docker", "bin", "grafana.sh", mode=0755)
    sudo("mkdir -p /var/lib/grafana")


@task()
def configure():
    '''
    Configure grafana
    :return:
    '''
    put_file("etc", "supervisor", "conf.d", "grafana.conf")
    run("supervisorctl update grafana")
    pass


@task
def install():
    '''
    Deploys & configures grafana
    :return:
    '''
    deploy()
    configure()
