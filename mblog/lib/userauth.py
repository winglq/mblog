import uuid

from mblog.lib.authenticate import BasicAuth
from mblog import exceptions 


class UserAuth:
    token_map = {}
    reverse_token_map = {}
    auth = BasicAuth()

    def authorize(self, user):
        return True

    def authenticate(self, usr=None, pwd=None, token=None):
        if usr and pwd:
            self.auth.authenticate(usr, pwd)
            if usr not in self.token_map:
                token = str(uuid.uuid4())
                self.token_map[usr] = token
                self.reverse_token_map[token] = usr
            return self.token_map[usr]
        if token:
            try:
                return self.reverse_token_map[token]
            except KeyError:
                raise exceptions.TokenNotExist()
