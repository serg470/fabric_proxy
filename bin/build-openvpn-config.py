#!/usr/bin/env python

import argparse
import os
import string
import sys

parser = argparse.ArgumentParser(
    prog="build-openvpn-config", description="Creates OpenVPN client config from easy_rsa PKI"
)

parser.add_argument('pki_dir', nargs=1, type=str, help="Path to easy_rsa PKI")
parser.add_argument('config_name', nargs=1, type=str, help="Name of configuration")
parser.add_argument("-o", "--output", nargs='?', type=str, help="Output to file (default to stdout)", default=None)

args = parser.parse_args()
pki_dir = args.pki_dir[0]
config_name = args.config_name[0]
output = args.output

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))

def read_fully(path):
    with open(path, 'r') as f:
        return f.read()


template = string.Template(read_fully(os.path.join(PROJECT_DIR, "templates", "openvpn", "user.ovpn")))
mapping = {
    "CA": read_fully(os.path.join(pki_dir, "ca.crt")),
    "CERT": read_fully(os.path.join(pki_dir, "issued", "%s.crt" % config_name)),
    "KEY": read_fully(os.path.join(pki_dir, "private", "%s.key" % config_name)),
}
res = template.substitute(mapping)

# Create dir if necessary
if output is not None:
    dir = os.path.dirname(output)
    if not os.path.exists(dir):
        os.makedirs(dir)
    f = open(output, 'w')
else:
    f = sys.stdout
f.write(res)
if f != sys.stdout:
    f.close()
