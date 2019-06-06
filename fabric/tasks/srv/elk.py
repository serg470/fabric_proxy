from lib.files import *
from lib.docker import *

@task()
def deploy():
    '''
    Deploy ELK
    :return:
    '''
    sudo("git clone https://github.com/deviantony/docker-elk /opt/elk/")
    sudo("cd /elk/cd/")
    sudo("docker-compose up -d")