import json

from mblog.stores.driver import StoreDriver
from mblog import exceptions


class User(object):

    _users = {}

    def __init__(self, username, store='file', location="/tmp/users.json"):
        self.location = location
        self.drv = StoreDriver.factory('file')
        self._username = username
        self.load()
        if username not in self._users:
            raise exceptions.UserNotExist(user=username)
        self._password = self._users[username]["password"]
        self._group = self._users[username]["group"]

    def load(self):
        if self._users:
            return
        f = self.drv.load(self.location)
        cnt = f.read().decode('utf-8')
        self._users = json.loads(cnt)

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def group(self):
        return self._group
