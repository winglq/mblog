import json

class Statistics(object):
    def on_post(self, req, resp):
        with open('/tmp/statistics.json', 'w') as f:
            f.write(req.stream.read())
            resp.body = "OK"

    def on_get(self, req, resp):
        with open('/tmp/statistics.json') as f:
            resp.body = f.read()
