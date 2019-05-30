from common import *


def install_service(service):
    """
    Enables & starts specified systemd service
    :return:
    """
    sudo("systemctl enable %s" % service, warn_only=True)
    sudo("systemctl start %s" % service, warn_only=True)


def reload_service(service):
    """
    Enables & starts systemd service
    :return:
    """
    sudo("systemctl enable %s" % service, warn_only=True)
    sudo("systemctl reload-or-restart %s" % service, warn_only=True)


def hard_restart_service(service):
    """
    Enables & starts systemd service
    :return:
    """
    sudo("systemctl enable %s" % service, warn_only=True)
    sudo("systemctl stop %s" % service, warn_only=True)
    sudo("systemctl start %s" % service, warn_only=True)

