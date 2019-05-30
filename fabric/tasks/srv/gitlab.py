from lib.files import *
from lib.docker import *
from fabric.api import *
from requests.auth import HTTPBasicAuth

import getpass
import json
import requests
import time
import re
import os


@task()
def deploy():
    """
    Deploy gitlab
    :return:
    """

    put_file("usr", "docker", "bin", "gitlab.sh", mode=0755)


@task()
def configure():
    """
    Configure gitlab
    :return:
    """

    put_file("etc", "supervisor", "conf.d", "gitlab.conf")
    sudo("supervisorctl update gitlab")

    gitlabURI = "http://gitlab.welespay.ru:8086/"

@task
def install():
    deploy()
    configure()

