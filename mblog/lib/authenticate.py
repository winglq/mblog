from mblog import exceptions
from mblog.lib.user import User


class Authenticate(object):
    def authenticate(self, usr, pwd):
        raise NotImplementedError()


class BasicAuth(object):
    def authenticate(self, usr, pwd):
        usr = User(usr)
        if pwd != usr.password:
            raise exceptions.PasswordInCorrect()
