from lib.files import *
from lib.common import *
from lib.docker import *
from fabric.contrib.files import exists, append
from fabric.api import *

path_to_domains_list = "/etc/letsencrypt/domains"
path_to_certs = "/secret/letsencrypt"

@task()
def install():
    """
    Installs EFF Certbot

    :return:
    """
    sudo("add-apt-repository ppa:certbot/certbot")
    sudo("apt-get -qy update && apt-get -qy install certbot")


@task()
def obtain_1st_cert():
    """
    Requests for certificate

    :return:
    """
    # Check if secret exists
    if not exists("/dev/mapper/secret", use_sudo=True):
        raise Exception("Secret volume is not mounted")
    sudo("mkdir -p %s" % path_to_certs)

    # Kill all processes that are using port 80, if any
    if int(sudo("lsof -t -i tcp:80 | wc -l")) > 0:
        sudo("lsof -t -i tcp:80 | xargs kill -9")

    list = domain_list()
    for i in range (0, len(list)):
        print (list[i])
        if not exists(path_to_certs + "/live/%s" % list[i]):
            path_to_curr_cert = path_to_certs + "/live/" + list[i]
            #sudo("mkdir -p %s" % path_to_curr_cert)
            sudo("certbot certonly --standalone --preferred-challenges http --config-dir %s --agree-tos \
                    -m helen.shafranova@gmail.com \
                    -d %s" % (path_to_certs, list[i]))


@task()
def renew_cert():
    """
    Certificate renewal

    :return:
    """
    # Check if secret exists
    if not exists("/dev/mapper/secret", use_sudo=True):
        raise Exception("Secret volume is not mounted")
    if not exists("/etc/cron.monthly/letsencrypt"):
        append("/etc/cron.monthly/letsencrypt", [
            "#!/bin/sh",
            "certbot --config-dir /secret/letsencrypt renew >> /var/log/letsencrypt/renew.log",
            "service nginx reload",
        ])

@task()
def deploy():
    """
    Installs EFF Certbot and requests for certificates

    :return:
    """
    install()
    obtain_1st_cert()


@task()
def add_domain(domain):
    """
    Adds a domain to the list of domains requiring SSL certificates
    
    :param domain: 
    :return: 
    """
    new_domain = path_to_domains_list + "/" + domain
    sudo("mkdir -p %s" % path_to_domains_list)
    if not exists(new_domain):
        sudo("touch %s" % new_domain)


@task()
def remove_domain(domain):
    """
    Removes a domain from the list of domains requiring SSL certificates

    :param domain:
    :return:
    """
    domain_to_delete = path_to_domains_list + "/" + domain
    if exists(domain_to_delete):
        sudo("rm -f %s" % domain_to_delete)


@task()
def domain_list():
    """
    Returns an array of domains requiring SSL certificate

    :return:
    """

    output = run("ls %s" % path_to_domains_list)
    files = output.split()
    return files

