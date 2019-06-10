from . import confd, consul, gitlab_runner, letsencrypt, \
    grafana, influxdb, nexus, nginx, postgres, telegraf, gitlab, ci, elk, rkn

from lib.common import *


@task
def kicksoft():
    """
    Performs setup containers to the host
    :return:
    """

    rkn.deploy()
    elk.deploy()
