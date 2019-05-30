from os import path
import posixpath

from common import *

LOCAL_PROJECT_DIR = path.dirname(path.dirname(path.dirname(__file__)))
LOCAL_FILES_DIR = path.join(LOCAL_PROJECT_DIR, "files")

VAR_DIR = posixpath.join("/var", "local", "fabric")
STAGE_DIR = posixpath.join(VAR_DIR, "stage")
DIST_DIR = posixpath.join(VAR_DIR, "dist")


def put_file(*paths, **kwargs):
    """
    Uploads specified file from project ``files/`` directory to the server & changes its owner

    :param paths: list of path components
    :param kwargs: additional arguments to pass to put (don't pass use_sudo here, since it's passed by default)
    :return:
    """
    local_path = path.join(LOCAL_FILES_DIR, *paths)
    remote_path = posixpath.join("/", *paths)
    sudo("mkdir -p %s" % posixpath.dirname(remote_path))
    put(local_path, remote_path, use_sudo=True, **kwargs)
    sudo("chown root %s" % remote_path)


def put_files(*paths, **kwargs):
    """
    Uploads specified files from project ``/files`` directory to the server & changes owner.
    The name of the files must be specified as the last argument in path, for example:

        put_files("usr", "local", "bin", "*")

    :param paths: list of path components
    :param kwargs: additional arguments to pass to put (don't pass use_sudo here, since it's passed by default)
    :return:
    """
    local_path = path.join(LOCAL_FILES_DIR, *paths)
    remote_path = posixpath.join("/", *paths[0:-1])
    sudo("mkdir -p %s" % remote_path)
    put(local_path, remote_path, use_sudo=True, **kwargs)
    sudo("chown root:root %s" % remote_path)


def rsync_files(*paths, **kwargs):
    """
    RSyncs a local directory to the server via temporary directory

    :param paths: list of subdirectories
    :param kwargs: additional arguments to pass to put (don't pass use_sudo here, since it's passed by default)
    :return:
    """
    user = whoami()
    local_path = path.join(LOCAL_FILES_DIR, *paths)
    remote_path = posixpath.join("/", *paths)
    remote_temp_path = posixpath.join(STAGE_DIR, *paths)
    mkdir_for(remote_temp_path, "%s:root" % user)
    rsync_project(remote_temp_path, path.join(local_path, "*"), delete=True)
    sudo("mkdir -p %s && rsync -r --delete %s %s" % (remote_path, posixpath.join(remote_temp_path, "*"), remote_path))
    # sudo("rm -r %s" % (remote_temp_path))


def mkdir_for(dir, owner="root:root"):
    """
    Creates a directory if it doesn't exist and sets specified owner to it
    :param dir:
    :param owner:
    :return:
    """
    return sudo("mkdir -p %s && sudo chown -R %s %s" % (dir, owner, dir))


def ln_overwrite(src, dest):
    """
    Creates symbolic link. If the destination already exists, deletes it
    :param src:
    :param dest:
    :return:
    """
    if exists(dest, use_sudo=True):
        sudo("rm %s && ln -s %s %s" % (dest, src, dest))
    else:
        sudo("ln -s %s %s" % (src, dest))


def is_mounted(volume):
    """
    Checks if volume is mounted
    :param volume:
    :return:
    """
    mounts = sudo("mount", quiet=True).split("\n")
    for m in mounts:
        if m.startswith(volume + " "):
            return True
    return False

