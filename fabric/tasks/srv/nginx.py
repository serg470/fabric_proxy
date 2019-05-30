import conf.server
from lib.common import *
from lib.files import *
from lib.services import *


# TODO: Move NGINX to Docker
@task()
def deploy(cert_path=None):
    """
    Deploy postgres
    :return:
    """
    # Check if secret is mounted
    if not exists("/dev/mapper/secret", use_sudo=True):
        raise Exception("Secret volume is not mounted")
    #sudo("mkdir -p /secret/nginx")

    # Copy keys if specified
    if cert_path is not None:
        put(path.join(cert_path, "fullchain.pem"), "/secret/letsencrypt/live/welespay.ru/fullchain.pem", mode=600, use_sudo=True)
        put(path.join(cert_path, "privkey.pem"), "/secret/letsencrypt/live/welespay.ru/privkey.pem", mode=600, use_sudo=True)

    # Key must exist
    if not exists("/secret/letsencrypt/live/welespay.ru/privkey.pem", use_sudo=True):
        raise Exception("Private key is not found on the server, specify cert_path param")

    # Configure DH params if necessary
    #if not exists("/secret/nginx/dhparam.pem", use_sudo=True):
    #    sudo("openssl dhparam -out /secret/nginx/dhparam.pem 2048")
    #sudo("chmod -R 600 /secret/nginx")

    # Install nginx
    sudo("apt-get -qy update && apt-get -qy upgrade && apt-get -qy install nginx")


@task()
def configure():
    """
    Configures nginx
    :return:
    """
    server = conf.server.current()
    put_file("etc", "nginx", "nginx.conf")
    put_files("etc", "nginx", "snippets", "*")
    sudo("rm /etc/nginx/sites-enabled/* && rm /etc/nginx/sites-available/default", warn_only=True)
    put_files("var", "www", "nginx-default", "*")
    for site in server.nginx_sites:
        put_file("etc", "nginx", "sites-available", site + ".conf")
        sa = posixpath.join("/etc", "nginx", "sites-available", site + ".conf")
        se = posixpath.join("/etc", "nginx", "sites-enabled", site + ".conf")
        sudo("ln -s %s %s" % (sa, se))
    reload_service("nginx")


@task
def templates():
    """
    Configure dynamic nginx from template via consul. KV:
    /config/nginx/ $service /enabled - MUST HAVE
    /config/route-manager/prod/services/ $service / $conf_name /external_zone - optional
    /config/route-manager/prod/services/" $service / $conf_name /vpn_zone - optional
    /config/nginx/ $service /upstream_port - MUST HAVE
    /config/nginx/ $service / $conf_name /keepalive - optional
    /config/nginx/ $service /allow_external - trigger, optional, "snippets/access-internal.conf;" will be use if not set
    /config/nginx/ $service /server_extra_includes - optional, "Raw text in server area"
    /config/nginx/" $service "/root_extra_includes - optional, "Raw test in root location area"
    :return:
    """
    put_file("etc", "confd", "templates", "nginx_services.conf.tmpl")
    put_file("etc", "confd", "conf.d", "nginx_services.conf.toml")
    sudo("rm -f /etc/nginx/sites-enabled/nginx_services.conf && /bin/true")
    sudo("ln -s /etc/nginx/sites-available/nginx_services.conf /etc/nginx/sites-enabled/nginx_services.conf")


@task()
def install(cert_path=None):
    """
    Deploy & configure nginx

    :param cert_path:
    :return:
    """
    deploy(cert_path)
    configure()


@task()
def reload():
    reload_service("nginx")


@task()
def deploy_proxy():
    """
    Deploy Nginx+Lua+Redis
    :return:
    """
    put_file("usr", "docker", "bin", "nginx-lua-redis.sh", mode=0755)


@task()
def configure_proxy():
    """
    Configure Nginx+Lua+Redis
    :return:
    """
    put_file("etc", "supervisor", "conf.d", "nginx-lua-redis.conf")
    run("supervisorctl update nginx-lua-redis")


@task
def install_proxy():
    """
    Deploys & configures Nginx+Lua+Redis
    :return:
    """
    deploy_proxy()
    configure_proxy()