
# Group names
SUDO_GROUP = 'sudo'
STAFF_GROUP = 'staff'
DOCKER_GROUP = 'docker'

GROUPS_TO_CREATE = [DOCKER_GROUP,]
DEFAULT_PASSWORD = '$1$7LdQYh.e$FHYx88v7B7m1/eYONCjeZ/'

class User:

    def __init__(self, name, password, authorized_keys, groups):
        '''

        :param name:                Unix user name
        :param password:            Encrypted password or None to set default
        :param authorized_keys      User's public keys (one key per line)
        :param groups:              The list of group names (XXX_GROUP constants)
        '''
        self.name = name
        self.password = password
        self.authorized_keys = authorized_keys
        self.groups = set(groups)


    def initial_password(self):
        if self.password is None:
            return DEFAULT_PASSWORD
        else:
            return self.password

USERS = [
    User('toor',
         '$6$QYgeESqN$qPPB17ysREbgnmqIKSG/jkWctWah5OsIx./tPNoGJoDPPE.BcG32CqPCAypZmo4rZoz4QUJuPdA92Svf6A13o0',
		 'ssh-rsa AAAAB3NzaC1yc2EAAAABJQAAAQEAnRezVC1TfZOX3JtAFB0idQOwJITq5EU/xM5R'
		 'jKstknarY4N1cg0fFG8QGvsUeIArNFvI9hd8xvHWI7UgYh/fY1VuNDLt5QmwNGWR'
		 'VrLlq7Hdh9nV6JFtFrAgaC3h4JvCc/eSfGQSwk3ou5VN/wCxktlKMgqnfdd5fPou'
		 't7Tw2zZvw0z0Iy9FjCz/mu7sF+3dnY9KItyDZqXdON3v/kFOziYB1wlJ1tE7Ii5d'
		 'QBvdw4ZyJdmSBFz/kW4Tv298TF3xeH35HjW33ydpTC63XHoh/RVQh3D+075+7HeQ'
		'1zDxRfqw9zPM4pGsezJOy4nzrRPqmGX50D9FSoXP5/u0+errmw== toor',
         [DOCKER_GROUP, STAFF_GROUP, SUDO_GROUP]),
]
