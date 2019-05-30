from lib.files import *
from lib.docker import *
from fabric.api import *
from requests.auth import HTTPBasicAuth

import getpass
import json
import requests
import time
import re
import os

@task()
def provision():
    '''
    Provision default sonatype nexus
    :return:
    '''

    nexusURI = "https://nexus.locahlost/service/rest/v1/script"

    i = 0

    contents = [
        "repository.createDockerHosted('docker-internal', 8082, 8083)",
        "import org.sonatype.nexus.blobstore.api.BlobStoreManager; " +
        "repository.createDockerProxy('docker-hub','https://registry1.docker.io'," +
        " 'HUB',null,null,null,BlobStoreManager.DEFAULT_BLOBSTORE_NAME,true,true,)",
        "repository.createDockerGroup('docker-all', 8084, null, ['docker-hub', 'docker-internal'], true)",
        "import org.sonatype.nexus.blobstore.api.BlobStoreManager; repository.createRawHosted('raw')",
        "security.addRole('reader','reader','reader'," +
        "['nx-repository-view-*-*-browse','nx-repository-view-*-*-read'], [''])",
        "security.setAnonymousAccess(Boolean.valueOf('False'))",
        "import org.sonatype.nexus.security.realm.RealmManager;" +
        " realmManager.enableRealm('DockerToken', 'Docker Bearer Token Realm')",
    ]

    for cont in contents:
        data = {
            "name": "n" + str(i),
            "type": "groovy",
            "content": cont
        }
        r = requests.post(nexusURI, auth=('admin', 'admin123'), verify=False,
                          headers={"Content-Type": "application/json"}, data=json.dumps(data))
        print(r.status_code)
        r = requests.post(nexusURI + "/n" + str(i) + "/run", auth=('admin', 'admin123'), verify=False,
                          headers={"Content-Type": "text/plain"})
        print(r.status_code)
        i += 1

    i1 = "security.addUser('reader', 'reader', 'read','root@localhost', true,'" \
         + getpass.getpass('Reader password:') + "', ['reader'])"
    data = {
        "name": "a1",
        "type": "groovy",
        "content": i1
    }
    r = requests.post(nexusURI, auth=('admin', 'admin123'), verify=False, headers={"Content-Type": "application/json"},
                      data=json.dumps(data))
    print(r.status_code)
    r = requests.post(nexusURI + "/a1/run", auth=('admin', 'admin123'), verify=False,
                      headers={"Content-Type": "text/plain"})
    print(r.status_code)

    i2 = "security.addUser('ci', 'writer', 'GITLAB-CI', 'root@localhost', true, '" + getpass.getpass(
        'Writer password') + "', ['nx-admin'])"
    data = {
        "name": "a2",
        "type": "groovy",
        "content": i2
    }
    r = requests.post(nexusURI, auth=('admin', 'admin123'), verify=False, headers={"Content-Type": "application/json"},
                      data=json.dumps(data))
    print(r.status_code)
    r = requests.post(nexusURI + "/a2/run", auth=('admin', 'admin123'), verify=False,
                      headers={"Content-Type": "text/plain"})
    print(r.status_code)

    i3 = "security.securitySystem.changePassword('admin', '" + getpass.getpass('Admin password') + "')"
    data = {
        "name": "a3",
        "type": "groovy",
        "content": i3
    }
    r = requests.post(nexusURI, auth=('admin', 'admin123'), verify=False, headers={"Content-Type": "application/json"},
                      data=json.dumps(data))
    print(r.status_code)
    r = requests.post(nexusURI + "/a3/run", auth=('admin', 'admin123'), verify=False,
                      headers={"Content-Type": "text/plain"})
    print(r.status_code)


@task()
def scrub(image, min_version):
    '''
    Remove outdated blobs from Docker
    :param image: 
    :param min_version: like 0.13.0
    :return:
    '''

    dockerURI = "https://docker-vpn.locahlost/"

    if os.environ.has_key("DOCKER_PWD"):
        print("Connecting to %s" % dockerURI)
    else:
        print("The DOCKER_PWD should be set")
        exit(-1)
    r = requests.get(dockerURI + "/v2/" + image + "/tags/list",
                     auth=HTTPBasicAuth('ci', str(os.environ['DOCKER_PWD'])),
                     headers={"Accept": "application/vnd.docker.distribution.manifest.v2+json"})

    # (\d+)\.(\d+)\.(\d+)-(\w+)-([0-9a-f]+)
    vers = re.search('(\\d+)\\.(\\d+)\\.(\\d+)', min_version)
    blobsave = set()
    blobreduce = set()

    if r.status_code > "400":
        print ("Auth issue. DOCKER_PWD should be set.")
        exit(-1)
    else:
        tags = json.loads(r.text)
        for t in tags["tags"]:
            desc = re.search("(\\d+)\\.(\\d+)\\.(\\d+)-(\\w+)-([0-9a-f]+)", str(t))
            if desc:
                if (desc.group(1) <= vers.group(1)) & (desc.group(2) <= vers.group(2)) & (
                        desc.group(3) <= vers.group(3)):
                    print("REDUCE:" + str(t))
                    getblobs = requests.get(dockerURI + "/v2/" + image + "/manifests/" + str(t),
                                            auth=HTTPBasicAuth('ci', str(os.environ['DOCKER_PWD'])),
                                            headers={
                                                "Accept": "application/vnd.docker.distribution.manifest.v2+json"})
                    blobsjson = json.loads(getblobs.text)
                    for blob in blobsjson["layers"]:
                        blobreduce.add(blob["digest"])
                else:
                    print("SAVE:" + str(t))
                    getblobs = requests.get(dockerURI + "/v2/" + image + "/manifests/" + str(t),
                                            auth=HTTPBasicAuth('ci', str(os.environ['DOCKER_PWD'])),
                                            headers={
                                                "Accept": "application/vnd.docker.distribution.manifest.v2+json"})
                    blobsjson = json.loads(getblobs.text)
                    for blob in blobsjson["layers"]:
                        blobsave.add(blob["digest"])

    blobsToDelete = set()
    blobsToDelete = blobreduce - blobsave
    for bl in blobsToDelete:
        r = requests.delete(dockerURI + "/v2/" + image + "/blobs/" + str(bl),
                            auth=HTTPBasicAuth('ci', str(os.environ['DOCKER_PWD'])),
                            headers={
                                "Accept": "application/vnd.docker.distribution.manifest.v2+json"})
        print(str(bl) + " = " + str(r.status_code))


@task()
def deploy():
    '''
    Deploy nexus
    :return:
    '''

    put_file("usr", "docker", "bin", "nexus.sh", mode=0755)


@task()
def configure():
    '''
    Configure sonatype nexus3
    :return:
    '''

    put_file("etc", "supervisor", "conf.d", "nexus.conf")
    sudo("supervisorctl update nexus")

    nexusURI = "https://nexus.locahlost/service/rest/v1/script"

    r = requests.get(nexusURI, auth=('admin', 'admin123'), verify=False)
    retry = 0
    while (r.status_code != "401" and r.status_code != "502") or retry > 20:
        if retry > 1:
            time.sleep(10)
        retry = +1
        r = requests.get(nexusURI, auth=('admin', 'admin123'), verify=False)
        if r.status_code == "200":
            provision()


@task
def install():
    deploy()
    configure()
