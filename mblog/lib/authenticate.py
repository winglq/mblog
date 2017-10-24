from mblog import exceptions
from mblog.lib.user import FileStoreUser


class Authenticate(object):
    def authenticate(self, usr, pwd):
        raise NotImplementedError()


class BasicAuth(object):
    def authenticate(self, usr, pwd):
        usr = FileStoreUser(usr)
        if pwd != usr.password:
            raise exceptions.PasswordInCorrect()
