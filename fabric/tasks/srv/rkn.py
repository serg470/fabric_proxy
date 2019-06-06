from lib.files import *
from lib.docker import *
import os
from fabric.contrib.files import exists

@task()
def deploy():
    '''
    Deploy RKN
    :return:
    '''
    if exists('/opt/rkn/', use_sudo=True):
        sudo("rm -rf /opt/rkn/")
    sudo("git clone https://github.com/serg470/filter.git /opt/rkn/")
 #   sudo("cd /opt/rkn/")
    sudo("docker-compose -f /opt/rkn/docker-compose.yml up -d")