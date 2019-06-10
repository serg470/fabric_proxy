from lib.files import *
from lib.services import *

@task
def deploy():
    '''
    Deploys base packages without configuring them
    :return:
    '''
    sudo("apt-get -qy update && apt-get -qy upgrade")
    # System tools
    sudo("apt-get -qy install git nano openvpn unzip ntp lsof mc net-tools")
    # Apt utilities
    sudo("apt-get -qy install apt-transport-https ca-certificates curl software-properties-common")
    # Docker
    sudo("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -")
    # XXX: This is for ubuntu 18.04
    put_file("etc", "apt", "sources.list.d", "docker-bionic.list")
    sudo("apt-get -qy update")
    sudo("apt-get -qy install docker-ce")

    # Docker-compose
    compose_version = sudo("curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d '\"' -f4")
    sudo('curl -L "https://github.com/docker/compose/releases/download/%s/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose' % compose_version)
    sudo("chmod +x /usr/local/bin/docker-compose")

    # Python packages
    sudo("apt-get -qy install python-setuptools python-pip python-dev software-properties-common")


@task
def configure():
    '''
    Configures base packages
    :return:
    '''
    # Set locale
    append("/etc/profile", "export LC_ALL=en_US.UTF-8", use_sudo=True)

    # Timezone
    sudo("rm /etc/localtime && ln -s /usr/share/zoneinfo/UTC /etc/localtime")
    sudo("dpkg-reconfigure -f noninteractive tzdata")

    # Docker
    install_service("docker")

@task
def install():
    '''
    Deploys & configures base packages
    :return:
    '''
    deploy()
    configure()


@task
def boot_sequence_setup():
    '''
    Disable systemd services due to secret mount
    :return:
    '''

    sudo("systemctl disable nginx")
    sudo("systemctl disable supervisord")
    sudo("systemctl disable confd")
    sudo("systemctl disable docker")


@task
def start_up():
    '''
    Use boot_sequence for application layer
    :return:
    '''
    sudo("systemctl start docker")
    sudo("systemctl start supervisord")
    sudo("systemctl start confd")
    sudo("systemctl start nginx")
    sudo("supervisorctl update")
#TODO: Postgresql should be started via consul or reschedule via supervisord