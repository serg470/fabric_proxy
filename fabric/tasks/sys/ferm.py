from lib.files import *
from lib.services import *

@task()
def deploy():
    """Deploy ferm firewall"""
    sudo("apt-get -qy update && apt-get -qy upgrade")
    sudo("DEBIAN_FRONTEND=noninteractive apt-get -qy install ferm")


@task()
def configure():
    """Apply ferm firewall configuration"""
    put_file("etc", "ferm", "ferm.conf")
    reload_service("ferm")


@task()
def install():
    """Deploy & configure ferm firewall"""
    deploy()
    configure()
