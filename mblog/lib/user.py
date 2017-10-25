import uuid


class User:
    name = "1"
    pwd = "10"
    grp = "admin"
    token_map = {}
    reverse_token_map = {}

    def authorize(self, token):
        usr = self.reverse_token_map.get(token, None)
        return usr

    def authenticate(self, usr, pwd):
        if usr == self.name and pwd == self.pwd:
            if usr not in self.token_map:
                token = str(uuid.uuid4())
                self.token_map[usr] = token
                self.reverse_token_map[token] = usr
            return self.token_map[usr]
