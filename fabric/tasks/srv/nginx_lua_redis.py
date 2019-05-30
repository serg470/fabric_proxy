from lib.files import *
from lib.docker import *


@task()
def deploy():
    """
    Deploy Nginx+Lua+Redis
    :return:
    """
    put_file("usr", "docker", "bin", "nginx-lua-redis.sh", mode=0755)


@task()
def configure():
    """
    Configure Nginx+Lua+Redis
    :return:
    """
    put_file("etc", "supervisor", "conf.d", "nginx-lua-redis.conf")
    run("supervisorctl update nginx-lua-redis")
    pass


@task
def install():
    """
    Deploys & configures Nginx+Lua+Redis
    :return:
    """
    deploy()
    configure()
