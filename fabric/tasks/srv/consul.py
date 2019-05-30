from lib.files import *
from lib.docker import *
import os
import string
import StringIO
import getpass


@task()
def deploy():
    '''
    Deploy consul agent
    :return:
    '''

    # Check if secret exists
    if not exists("/dev/mapper/secret", use_sudo=True):
        raise Exception("Secret volume is not mounted")
    if not exists("/secret/consul/encrypt.json", use_sudo=True):

        sudo("mkdir -p /secret/consul")
        sudo("chmod 0700 /secret/consul")
        template = string.Template(
            read_fully(os.path.join(LOCAL_PROJECT_DIR, "templates", "consul", "encrypt.json")))
        mapping = {
            "KEY": getpass.getpass('Enter Consul encrypt password:'),
        }
        res = template.substitute(mapping)

        output = StringIO.StringIO()
        output.write(res)
        put(output, '/secret/consul/encrypt.json', use_sudo=True)
        output.close()
        sudo("chmod 644 /secret/consul/encrypt.json")

    put_file("usr", "docker", "bin", "consul.sh", mode=0755)


def read_fully(path):
    with open(path, 'r') as f:
        return f.read()


@task()
def configure():
    '''
    Configure consul
    :return:
    '''
    put_file("etc", "supervisor", "conf.d", "consul.conf")
    run("supervisorctl update consul")
    pass


@task
def install():
    '''
    Deploys & configures consul
    :return:
    '''
    deploy()
    configure()
