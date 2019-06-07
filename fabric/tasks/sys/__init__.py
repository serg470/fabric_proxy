from lib.common import *

from . import base,cron,docker,openvpn,users

@task
def kickstart():
    """
    Performs initial setup of the server: partitions, base packages, users, etc
    :return:
    """
    users.configure()
    base.install()



