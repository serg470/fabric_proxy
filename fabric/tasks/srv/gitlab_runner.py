from lib.docker import *
from lib.files import *
from lib.services import *


@task()
def deploy():
    """
    Deploy gitlab-runner-agent from official site

    :return:
    """

    sudo("apt-get update")
    sudo("apt-get install curl")
    sudo("curl -L https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh | sudo bash")
    sudo("apt-get update")
    sudo("apt-get install gitlab-runner")
    install_service("gitlab-runner")


@task()
def configure():
    """
    Configure gitlab-runner-agent

    :return:
    """

    # Runner for frontend
    sudo('gitlab-runner register --non-interactive --executor docker --docker-image "docker:stable" \
         --url "https://gitlab.welespay.ru" --registration-token "am6xcEeH7hWexWford5b" \
         --description "frontend-runner" --tag-list "frontend-runner" --docker-privileged')

    # Runner for backend
    sudo('gitlab-runner register --non-interactive --executor docker --docker-image "docker:stable" \
         --url "https://gitlab.welespay.ru" --registration-token "TUvuqF8wcYqefdJ5uJJx" \
         --description "backend-runner" --tag-list "backend-runner" --docker-privileged')


    # Runner for backendbuild
    sudo('gitlab-runner register --non-interactive --executor docker --docker-image "docker:stable" \
         --url "https://gitlab.welespay.ru" --registration-token "4zUpzcdUyt2HWis3V-oj" \
         --description "backendbuild-runner" --tag-list "backendbuild-runner" --docker-privileged')

    reload_service("gitlab-runner")


@task
def install():
    """
    Deploy & configure gitlab-runner-agent

    :return:
    """
    deploy()
    configure()
