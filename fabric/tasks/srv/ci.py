from lib.files import *
from lib.docker import *


@task()
def push():
    """
    Push CI files to server
    :return:
    """
    put_file("usr", "local", "bin", "deploy.sh", mode=0755)
    put_file("usr", "local", "bin", "docker-compose.yml", mode=0644)
