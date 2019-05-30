from lib.common import *
from lib.files import *
import conf.user

@task
def configure():
    '''
    Performs configuration of users: reset password, set groups, login shell & authorized keys
    :return:
    '''
    configure_groups()
    configure_users()


@task
def configure_groups():
    for group in conf.user.GROUPS_TO_CREATE:
        if not group_exists(group):
            run("groupadd %s" % group)


@task
def configure_users():
    created_users = []
    for user in conf.user.USERS:
        groups = ",".join(user.groups)
        if not user_exists(user.name):
            run("useradd -s /bin/bash -m -g %s -G %s %s" % (conf.user.STAFF_GROUP, groups, user.name))
            created_users.append(user)
        else:
            run("usermod -s /bin/bash -g %s -G %s %s" % (conf.user.STAFF_GROUP, groups, user.name))
        append(posixpath.join("/home", user.name, ".profile"), "umask 002", use_sudo=False)
        write_authorized_keys(user.name, user.authorized_keys)
    passwords = "".join(["%s:%s\n" % (user.name, user.initial_password()) for user in conf.user.USERS])
    temp_file = run("mktemp")
    passwords_file = StringIO.StringIO(passwords)
    put(passwords_file, temp_file, use_sudo=False)
    run("chpasswd -e < %s" % temp_file)
    run("rm %s" % temp_file)

    # Require password change from created users
    for user in created_users:
        if user.password is None:
            run("chage -d 0 %s" % (user.name))

    # Remove root auth_keys
    run("rm /root/.ssh/authorized_keys", warn_only=True)
    run("apt-get -qy update && apt-get -qy install sudo")


def write_authorized_keys(user_name, ak):
    ak_file = StringIO.StringIO(ak)
    ssh_path = posixpath.join("/home", user_name, ".ssh")
    ak_path = posixpath.join(ssh_path, "authorized_keys")
    run("mkdir -p %s && chown %s:%s %s && chmod 700 %s" % (ssh_path, user_name, conf.user.STAFF_GROUP, ssh_path, ssh_path))
    put(ak_file, ak_path, use_sudo=False)
    run("chown %s:%s %s && chmod 600 %s" % (user_name, conf.user.STAFF_GROUP, ak_path, ak_path))
