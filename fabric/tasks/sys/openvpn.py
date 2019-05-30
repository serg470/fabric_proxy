from lib.files import *
from lib.services import *
import conf.server


@task
def configure(pki_dir=None):
    '''
    Configure OpenVPN on the host
    :return:
    '''
    srv = conf.server.current()
    conf_name = "server" if srv.openvpn_server else "client"
    service_name = "openvpn@%s.service" % conf_name

    # Check if secret volume is mounted
    if not is_mounted("/dev/mapper/secret"):
        raise Exception("Secret volume must be mounted")
    if pki_dir is not None:
        upload_files(srv.name, conf_name, pki_dir)
    else:
        print("pki_dir is empty, won't copy keys")

    # Put configs
    if srv.openvpn_server:
        put_file("etc", "openvpn", "server.conf")
        put_files("etc", "openvpn", "clients", "*")
    else:
        put_file("etc", "openvpn", "client.conf")

    # Restart service
    hard_restart_service(service_name)


@task
def install(pki_dir=None):
    '''
    Configure OpenVPN on the host
    :return:
    '''
    configure(pki_dir)


@task
def reload():
    srv = conf.server.current()
    conf_name = "server" if srv.openvpn_server else "client"
    service_name = "openvpn@%s.service" % conf_name
    hard_restart_service(service_name)


def upload_files(host_name, config_name, pki_dir):
    """
    Uploads server keys & certificates.

    It's required to upload these files before configuring the server

    :param pki_dir:
    :return:
    """
    sudo("mkdir -p /secret/openvpn")
    put(path.join(pki_dir, "ca.crt"), "/secret/openvpn/ca.crt", use_sudo=True)
    put(path.join(pki_dir, "dh.pem"), "/secret/openvpn/dh.pem", use_sudo=True)
    put(path.join(pki_dir, "issued", host_name + ".crt"), "/secret/openvpn/%s.crt" % config_name, use_sudo=True)
    put(path.join(pki_dir, "private", host_name + ".key"), "/secret/openvpn/%s.key" % config_name, use_sudo=True)
    sudo("chown -R root:root /secret/openvpn")
    sudo("chmod -R 400 /secret/openvpn")
