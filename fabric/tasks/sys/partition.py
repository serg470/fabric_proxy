from lib.common import *
from lib.files import *
import conf.server
from fabric.contrib.console import confirm
from fabric.api import *
from fabric.contrib.files import append,exists,sed,comment


@task()
def configure():
    """
    Performs initial configuration of partitions

    :return:
    """
    configure_swap()
    configure_mirror()
    configure_striped()


@task()
def configure_swap():
    """
    Configures swap

    :return:
    """
    sudo("swapoff /dev/md0", warn_only=True)

    # Make swap Raid0
    recreate_raid("/dev/md0", 0, ["/dev/sda1", "/dev/sdb1"])
    # Encrypt swap with random key
    append("/etc/crypttab", ("swap  /dev/md0  /dev/urandom  swap,cipher=aes-xts-plain64,size=256"), use_sudo=True)
    comment("/etc/fstab", "/dev/md/0 none swap sw 0 0", backup=None, use_sudo=True)
    append("/etc/fstab", ("/dev/mapper/swap none swap sw 0 0"), use_sudo=True)
    finalize_configuration()


@task()
def configure_striped():
    """
    Configures /striped partition

    :return:
    """
    # TODO: Add external lock to protect from accidental running
    srv = conf.server.current()
    if not srv.has_striped:
        return
    sudo("umount /dev/md4", warn_only=True)
    recreate_raid("/dev/md4", 0, ["/dev/sda5", "/dev/sdb5"])
    sudo("mkfs.ext4 -F /dev/md4")
    sudo("mount /dev/md4 /striped")
    finalize_configuration()


@task()
def configure_mirror():
    """
    Configures /mirror partition

    :return:
    """
    # TODO: Add external lock to protect from accidental running
    srv = conf.server.current()
    if not srv.has_striped:
        return
    sudo("umount /dev/md3", warn_only=True)
    recreate_raid("/dev/md3", 1, ["/dev/sda4", "/dev/sdb4"])
    sudo("mkfs.ext4 -F /dev/md3")
    sudo("mount /dev/md3 /mirror")
    finalize_configuration()


@task()
def create_secret(size_mb=1024, file_name="/mirror/secret.bin", device_name="secret", mount_point="/secret"):
    """
    Creates & opens vault for secrets

    :return:
    """
    if exists("%s" % file_name, use_sudo=True) and not confirm("Secret file exists. Choose Y to overwrite, N to exit.", default=False):
        return
    if exists("/dev/mapper/%s" % device_name):
        sudo("cryptsetup luksClose %s" % device_name)
    sudo("dd if=/dev/zero bs=1M count=%d of=%s" % (size_mb, file_name))
    sudo("cryptsetup luksFormat %s" % file_name)
    sudo("cryptsetup luksOpen %s %s" % (file_name, device_name))
    sudo("sudo mkfs.ext4 /dev/mapper/%s" % device_name)
    sudo("mkdir -p %s" % mount_point)
    sudo("mount /dev/mapper/%s %s" % (device_name, mount_point))
    sudo("chmod 700 %s" % mount_point)


@task()
def open_secret(file_name="/mirror/secret.bin", device_name="secret", mount_point="/secret"):
    """
    Opens vault for secrets

    :param file_name:
    :param device_name:
    :param mount_point:
    :return:
    """
    if exists("/dev/mapper/%s" % device_name):
        sudo("cryptsetup luksClose %s" % device_name)
    sudo("cryptsetup luksOpen %s %s" % (file_name, device_name))
    sudo("mkdir -p %s" % mount_point)
    sudo("mount /dev/mapper/%s %s" % (device_name, mount_point))


@task()
def close_secret(device_name="secret"):
    """
    Opens vault for secrets

    :param device_name:
    :return:
    """
    sudo("umount /dev/mapper/%s" % device_name)
    sudo("cryptsetup luksClose %s" % device_name, warn_only=True)


@task()
def recreate_raid(device, level, volumes):
    """
    Recreates raid device with specified level.
    The device must not be mounted
    Note: created devices must be formatted/mounted externally,

    :param device:
    :param level:
    :param volumes:
    :return:
    """
    # TODO: Add external lock to protect from accidental running
    sudo("mdadm --stop %s && mdadm --remove %s" % (device, device))
    sudo("mdadm --zero-superblock %s" % " ".join(volumes))
    sudo("mdadm --create --verbose %s --level=%d --raid-devices=%d %s" % (device, level, len(volumes), " ".join(volumes)))


@task()
def finalize_configuration():
    """
    Finalizes configuration after partitioning

    :return:
    """
    sudo("/usr/share/mdadm/mkconf > /etc/mdadm/mdadm.conf")
    sudo("update-initramfs -u")
