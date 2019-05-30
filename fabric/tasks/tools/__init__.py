from lib.common import *


@task
def df():
    '''
    Show file system space usage
    :return:
    '''
    sudo("df -h")


@task
def restart():
    '''
    Initiates restart of the server
    :return:
    '''
    sudo("shutdown -r now")
