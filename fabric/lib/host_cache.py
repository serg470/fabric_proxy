from fabric.api import env


class HostCache(object):

    def __init__(self, func):
        self.func = func
        self.map = {}

    def get(self):
        host = env['host']
        if host in self.map:
            return self.map[host]
        else:
            self.map[host] = self.func()
            return self.map[host]
