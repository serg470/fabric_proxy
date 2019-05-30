
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
    User('serg',
         '$6$4sknD8w5$aVIzIrFW.VdDF5YYXcwdSh15jM67ZV/khv8UyD7375rImiqk.7GbNs4.oYenpaksXOEwOB6vk865B3v/5nwEj0',
		 'ssh-rsa AAAAB3NzaC1yc2EAAAABJQAAAQEAnRezVC1TfZOX3JtAFB0idQOwJITq5EU/xM5R'
		 'jKstknarY4N1cg0fFG8QGvsUeIArNFvI9hd8xvHWI7UgYh/fY1VuNDLt5QmwNGWR'
		 'VrLlq7Hdh9nV6JFtFrAgaC3h4JvCc/eSfGQSwk3ou5VN/wCxktlKMgqnfdd5fPou'
		 't7Tw2zZvw0z0Iy9FjCz/mu7sF+3dnY9KItyDZqXdON3v/kFOziYB1wlJ1tE7Ii5d'
		 'QBvdw4ZyJdmSBFz/kW4Tv298TF3xeH35HjW33ydpTC63XHoh/RVQh3D+075+7HeQ'
		'1zDxRfqw9zPM4pGsezJOy4nzrRPqmGX50D9FSoXP5/u0+errmw== serg',
         [DOCKER_GROUP, STAFF_GROUP, SUDO_GROUP]),
    User('dh',
         '$6$ly0hIZlr$Pk6bKI9mLYDS7fWHo6qjRTYaWkDuwDwxnVxHUz72N1df3xf4gL2muyv2Bc5eF23peSyOnESj9emMGJqjPC4A71',
         'ssh-rsa AAAAB3NzaC1yc2EAAAABJQAAAQEA6nZbqRoYfaxmVmcGavZ1F+MSns+mIQ6J4Re0NGNz9uc1r0EkFdpU7qGpQbfR70YsoYr8hjjD2f'
         'lJpjlNF4ov3xALANYkYI+3Ab7aqulXiQ/U4EL0lPC/aKrVGT6os/KGbgIFs8NeBC2vmVdrIWraubxaA6ZBHRnBUdU5UQ0Vss5CW/LWVF6/mPnc'
         'vkSHjLhbhSyKDP+NF0FodohNe1ux2tIbyo6uVH+7+Bi5qrSipPxXJVNjI/pccFoAIJCGLzek1u39bWnr2pw1wTauKElN/dwKUcBaIHMlbVqt8c'
         'SotBHrTbo4CO9O3yG5PtP/Acy6NkERU/wV7a09zS0zY4JkBQ== dh',
         [DOCKER_GROUP, STAFF_GROUP, SUDO_GROUP])
]
