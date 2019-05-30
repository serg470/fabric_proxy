from lib.files import *
from lib.common import *
import os.path


@task
def configure():
    '''
    Configures cron packages with override root crontab
    :return:
    '''

    host_file = server_name(env.host) + ".conf"
    common_file = "common.conf"

    if os.path.isfile(LOCAL_FILES_DIR + '/var/cron.d/' + host_file):
        put_files("var", "cron.d",  host_file)
    put_files("var", "cron.d", common_file)

    if not exists("/var/cron.d/" + host_file, use_sudo=True):
        sudo("EDITOR='tee' cat /var/cron.d/" + common_file + "| grep -v '^#' | sort --unique | crontab - ")
    else:
        sudo("EDITOR='tee' cat /var/cron.d/" + host_file + " /var/cron.d/" +
             common_file + "| grep -v '^#' | sort --unique | crontab - ")


@task
def install():
    '''
    Configures cron packages
    :return:
    '''

    configure()
