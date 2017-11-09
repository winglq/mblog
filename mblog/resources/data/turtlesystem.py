import json


class TurtleSystem(object):
    def on_post(self, req, resp, sysnum):
        with open('/tmp/stock_system%s.json' % sysnum, 'w') as f:
            f.write(req.stream.read())
        resp.body = "OK"

    def on_get(self, req, resp, sysnum):
        with open('/tmp/stock_system%s.json' % sysnum) as f:
            resp.body = f.read()
