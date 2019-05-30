from lib.common import *
import conf.server

IMAGE = '/root/images/Debian-99-stretch-64-minimal.tar.gz'

# TODO: Add external per-server partitioning configuration
PARTITIONS_DEFAULT = [
    'swap:swap:8G',        # This will become 8G swap on two partitions
    '/boot:ext2:2G',
    '/:ext4:1000G',
    '/mirror:ext4:1000G',
    '/striped:ext4:all',       # This will be changed to RAID0
]

PARTITIONS_NO_STRIPED = [
    'swap:swap:8G',        # This will become 8G swap on two partitions
    '/boot:ext2:512M',
    '/:ext4:all',
]


@task()
def deploy():
    '''
    Deploy default OS/Filesystem on Hetzner server. Works only in rescue system
    :return:
    '''
    srv = conf.server.current()
    sn = srv.name
    parts = ",".join(PARTITIONS_DEFAULT) if srv.has_striped else ",".join(PARTITIONS_NO_STRIPED)

    # TODO: Add external lock to protect from accidental running
    # Install image
    run("/root/.oldroot/nfs/install/installimage -n %s -r yes -l 1 -p %s -i %s -K /root/.ssh/robot_user_keys -a" % (sn, parts, IMAGE), shell=False)

    # Reboot
    run("shutdown -r now")

