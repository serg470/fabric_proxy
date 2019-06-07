from lib.common import *


# TODO: Extract configuration to external storage
class Server:
    def __init__(self, name, nginx_sites=[], has_striped=False, openvpn_server=False):
        self.name = name
        self.nginx_sites = nginx_sites
        self.has_striped = has_striped
        self.openvpn_server = openvpn_server


SERVERS = [

    # Infrastructure

    Server('extproxy',
           nginx_sites=['default','docker','nexus','gitlab','rancher']),
]

SERVER_MAP = dict([(s.name, s) for s in SERVERS])


def current():
    sn = server_name(env.host)
    if not SERVER_MAP.has_key(sn):
        raise Exception("Configuration for server %s not defined" % sn)
    return SERVER_MAP[sn]
