import falcon

from mblog.hooks.authorize import authorize


class Host(object):
    @falcon.before(authorize)
    def on_get(self, req, resp):
        with open('/tmp/remote_acess.txt', 'r') as f:
            resp.body = f.readlines()[-1]
