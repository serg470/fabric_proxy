import StringIO
import urlparse

from fabric.api import env,put,run,sudo,task
from fabric.contrib.files import append,exists,sed,comment
from fabric.contrib.project import rsync_project

from host_cache import HostCache


def server_name(host):
    suffixes = [".intertransl.com"]
    for s in suffixes:
        if host.endswith(s):
            return host[:-len(s)]
    raise ValueError("Don't know how to parse host name: %s" % host)


WHOAMI_CACHE = HostCache(lambda: run("whoami"))


def whoami():
    return WHOAMI_CACHE.get()


UNAME_CACHE = HostCache(lambda: run("uname"))


def uname():
    return UNAME_CACHE.get()


def user_exists(user_name):
    os = uname()
    if os == "Linux":
        res = sudo("id -u %s" % user_name, warn_only=True, quiet=True)
    elif os == "Darwin":
        res = sudo("dscl . -read /Users/%s" % user_name, warn_only=True, quiet=True)
    else:
        raise EnvironmentError("Don't know how to check if user exists on OS %s" % os)
    return res.return_code == 0


def group_exists(group_name):
    os = uname()
    if os == "Linux":
        res = sudo("getent group %s" % group_name, warn_only=True, quiet=True)
    elif os == "Darwin":
        res = sudo("dscl . -read /Groups/%s" % group_name, warn_only=True, quiet=True)
    else:
        raise EnvironmentError("Don't know how to check if group exists on OS %s" % os)
    return res.return_code == 0
