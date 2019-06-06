from lib.files import *
from lib.docker import *

@task()
def deploy():
    '''
    Deploy RKN
    :return:
    '''
    sudo("git clone https://github.com/serg470/filter.git /opt/rkn/")
    sudo("cd /opt/rkn/")
    sudo("docker-compose up -d")