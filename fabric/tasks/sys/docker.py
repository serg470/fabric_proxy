from lib.files import *
from lib.common import *
from fabric.contrib.files import exists
from fabric.api import *


@task()
def storage_configure(path_to_docker="/mirror/docker"):
    """
    Configure docker

    :param path_to_docker:
    :return:
    """
    sudo("systemctl stop docker")
    if run("pgrep dockerd", warn_only=True).succeeded == 0:
        date = run("date +%Y-%m-%d_%H-%M-%S")
        sudo("mkdir -p %s" % path_to_docker)
        if exists("/etc/docker/daemon.json", use_sudo=True):
            backup = '/etc/docker/daemon.json' + date
            sudo("mv /etc/docker/daemon.json %s" % backup)
        put_file("etc", "docker", "daemon.json")
        docker_storage_is_empty = run("ls -f %s | head -3 | wc -l" % path_to_docker)
        if int(docker_storage_is_empty) < 3:
            sudo("tar cf - -C /var/lib/docker . | tar xpvf - -C %s" % path_to_docker)
        new_path = '/var/lib/docker_' + date
        sudo("mv /var/lib/docker %s" % new_path)
        sudo("ln -s %s /var/lib" % path_to_docker)
        sudo("systemctl start docker")
        if run("pgrep dockerd", warn_only=True).succeeded == 0:
            raise Exception("Could not start docker daemon")
    else:
        raise Exception("Could not stop docker daemon")
