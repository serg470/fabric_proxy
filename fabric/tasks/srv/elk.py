from lib.files import *
from lib.docker import *

@task()
def deploy():
    '''
    Deploy ELK
    :return:
    '''
    if exists('/opt/elk/', use_sudo=True):
        sudo("rm -rf /opt/elk/")
    sudo("git clone https://github.com/serg470/elk.git /opt/elk/")
    sudo("export ELK_VERSION=7.0.1")
    sudo("docker-compose -f /opt/elk/docker-compose.yml up -d")
    sudo("sleep 1m")
    sudo("docker-compose -f /opt/elk/docker-compose.yml exec -T elasticsearch 'bin/elasticsearch-setup-passwords' auto --batch > /opt/elk/passwd")
    sudo("cat /opt/elk/passwd | grep = | tail -1 | cut -d' ' -f4 > /opt/elk/elastic")
    put_file("usr", "elk", "bin", "elk.sh", mode=0755)
    sudo("/usr/elk/bin/elk.sh")
    sudo("docker-compose -f /opt/elk/docker-compose.yml restart")

