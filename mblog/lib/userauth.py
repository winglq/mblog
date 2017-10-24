import uuid

from mblog.lib.authenticate import BasicAuth


class UserAuth:
    token_map = {}
    reverse_token_map = {}
    auth = BasicAuth()

    def authorize(self, token):
        usr = self.reverse_token_map.get(token, None)
        return usr

    def authenticate(self, usr, pwd):
        if self.auth.authenticate(usr, pwd):
            if usr not in self.token_map:
                token = str(uuid.uuid4())
                self.token_map[usr] = token
                self.reverse_token_map[token] = usr
            return self.token_map[usr]
