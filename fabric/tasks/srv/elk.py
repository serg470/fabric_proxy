from lib.files import *
from lib.docker import *
from io import BytesIO


@task()
def deploy():
    '''
    Deploy ELK
    :return:
    '''
    sudo("clean")
    if exists('/opt/elk/', use_sudo=True):
        sudo("rm -rf /opt/elk/")
    sudo("git clone https://github.com/serg470/elk.git /opt/elk/")
    sudo("docker-compose -f /opt/elk/docker-compose.yml up -d")
    sudo("sleep 1m")
    sudo("docker-compose -f /opt/elk/docker-compose.yml exec -T elasticsearch 'bin/elasticsearch-setup-passwords' auto --batch > /opt/elk/passwd")
    sudo("cat /opt/elk/passwd | grep = | tail -1 | cut -d' ' -f4 > /opt/elk/elastic")
    passwd = (read_file("/opt/elk/elastic")).rstrip()
    sudo("sed -i 's/changeme/%s/g' /opt/elk/kibana/config/kibana.yml" % passwd)
    sudo("sed -i 's/changeme/%s/g' /opt/elk/logstash/config/logstash.yml" % passwd)
    sudo("sed -i 's/changeme/%s/g' /opt/elk/logstash/pipeline/logstash.conf" % passwd)
    sudo("docker-compose -f /opt/elk/docker-compose.yml restart")
    sudo("sleep 1m")
#    sudo("curl -X POST 'http://extproxy.intertransl.com:5601/api/spaces/space' -u elastic:%s -H 'kbn-xsrf: true' -H 'Content-Type: application/json' -d\'{"id"}\'" % passwd)
    put_file("usr", "elk", "bin", "elk.sh", mode=0755)
    sudo("/usr/elk/bin/elk.sh")



def read_file(file_path, encoding='utf-8'):
    io_obj = BytesIO()
    get(file_path, io_obj)
    return io_obj.getvalue().decode(encoding)