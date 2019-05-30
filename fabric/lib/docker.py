from files import *
from common import *
from fabric.api import *

DOCKERFILES_DIR = posixpath.join(VAR_DIR, "dockerfiles")


def rsync_dockerfiles():
    """
    RSyncs project's Docker sources to the server

    :return:
    """
    user = whoami()
    local_path = path.join(LOCAL_PROJECT_DIR, "dockerfiles")
    mkdir_for(DOCKERFILES_DIR, "%s:root" % user)
    rsync_project(DOCKERFILES_DIR, path.join(local_path, "*"), delete=True)


def build_image(subdir, *tags):
    """
    Builds docker image from specified subdirectory & tag it

    :param subdir:
    :param tags:
    :return:
    """
    path = posixpath.join(DOCKERFILES_DIR, subdir)
    tags_str = " ".join(["--tag %s " % tag for tag in tags])
    sudo("docker build %s %s" % (path, tags_str))


def docker_login():
    """
    Login on docker with RO permissions

    :return:
    """
    run("docker login -u reader -p PWD HOST")


def docker_reader_root_auth():
    """
    Readonly login to docker.locahlost
    :return:
    """

    sudo("su - -c 'docker login -u reader -p PWD HOST'")


def docker_tag(image_name, tag):
    """
    Get and tag image as :latest

    :param image_name:
    :param tag:
    :return:
    """

    docker_login()

    run("docker pull %s" % image_name)
    img_split = image_name.split(':')
    img = str(img_split[0])
    tags = image_name + " " + img + ":" + tag
    run("docker tag %s" % tags)
