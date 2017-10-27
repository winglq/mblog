import uuid

from mblog.lib.authenticate import BasicAuth
from mblog.lib.authorize import Authorize
from mblog import exceptions 


class UserAuth:
    token_map = {}
    reverse_token_map = {}
    authen = BasicAuth()
    authorize = Authorize()

    def authorize(self, user, resource):
        authorize.authorize(user, resource)

    def authenticate(self, usr=None, pwd=None, token=None):
        if usr and pwd:
            self.authen.authenticate(usr, pwd)
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
