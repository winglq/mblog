import falcon

from mblog.hooks.authorize import authorize
from mblog.resources.resourcebase import ReourceBase


class Host(ReourceBase):
    @falcon.before(authorize)
    def on_get(self, req, resp):
        with open('/tmp/remote_acess.txt', 'r') as f:
            resp.body = f.readlines()[-1]

    def get_rule(self, req=None):
        return "owner"

    def get_owner(self, req=None):
        return "qing"
