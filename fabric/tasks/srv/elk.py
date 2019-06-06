from lib.files import *
from lib.docker import *

ELK_VERSION = "7.0.1"

@task()
def deploy():
    '''
    Deploy ELK
    :return:
    '''
    if exists('/opt/elk/', use_sudo=True):
        sudo("rm -rf /opt/elk/")
    sudo("git clone https://github.com/serg470/elk.git /opt/elk/")
    sudo("export ELK_VERSION=7.0.1")
    sudo("docker-compose -f /opt/elk/docker-compose.yml up -d")