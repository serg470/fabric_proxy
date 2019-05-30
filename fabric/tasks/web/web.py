from lib.files import *
from lib.docker import *
from fabric.api import prompt


@task()
def deploy():
    """
    :return:
    """
    # TODO: Change to connecting to artifacts repo at some point


@task()
def configure():
    """
    :return:
    """
    pass


@task()
def pull(tag='latest'):
    """
    Pulls specified image and tags it as current
    :return:
    """
    docker_login()
    docker_tag("docker.localhost/web:" + tag, 'current')


@task()
def restart():
    """
    Restart web application
    :return:
    """
    run("supervisorctl restart web")
    pass


@task()
def install():
    """
    Deploy & configure web
    :return:
    """
    deploy()
    configure()
