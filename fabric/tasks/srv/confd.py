from lib.common import *
from lib.files import *
from lib.services import *
from lib.docker import *

CONFD_VERSION = "0.16.0"
CONFD_SHA256 = "255d2559f3824dd64df059bdc533fd6b697c070db603c76aaf8d1d5e6b0cc334"


@task()
def deploy():
    """
    Deploy confd and create necessary folders
    :return:
    """
    # Check if secret is mounted
    sudo("mkdir -p /etc/confd/conf.d")
    sudo("mkdir -p /etc/confd/templates")
    sudo("mkdir -p /usr/local/bin")

    link = "https://github.com/kelseyhightower/confd/releases/download/v" + CONFD_VERSION + "/confd-" \
           + CONFD_VERSION + "-linux-amd64"

    sudo("wget -q -O /tmp/confd %s" % link)
    check_sha256 = "echo '" + CONFD_SHA256 + " /tmp/confd' | sha256sum --check -"
    run(check_sha256)
    sudo("mv /tmp/confd /usr/bin/confd && chmod 755 /usr/bin/confd")


@task()
def configure():
    """
    Configures confd

    :return:
    """

    put_file("etc", "systemd", "system", "confd.service")
    put_file("usr", "local", "bin", "confd.sh")
    sudo("chmod 755 /usr/local/bin/confd.sh")
    put_file("etc", "confd", "conf.d", "confd_services.conf.toml")
    put_file("etc", "confd", "templates", "confd_services.conf.tmpl")
    put_file("usr", "docker", "bin", "service.sh")
    sudo("chmod 755 /usr/docker/bin/service.sh")
    sudo("systemctl daemon-reload")
    docker_reader_root_auth()
    reload_service("confd")



@task()
def install():
    """
    Deploy & configure confd

    :return:
    """
    deploy()
    configure()


@task
def reload():
    reload_service("confd")
