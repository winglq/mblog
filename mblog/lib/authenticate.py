from mblog.lib.user import User


class Authenticate(object):
    def authenticate(self, usr, pwd):
        raise NotImplementedError()


class BasicAuth(object):
    def authenticate(self, usr, pwd):
        usr = User(usr)
        if pwd != usr.password:
            return False
        return True
