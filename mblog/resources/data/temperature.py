class Temperature(object):
    def on_get(self, req, resp, data=None):
        if data:
            with open('/tmp/temperature.txt', 'wa') as f:
                f.writelines([str(data)])
                resp.body = "OK"
            with open('/tmp/remote_acess.txt', 'wa') as f:
                f.writelines(req.access_route)
        else:
            with open('/tmp/temperature.txt', 'r') as f:
                resp.body = f.readlines()[-1]
