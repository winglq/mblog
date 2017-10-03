class Host(object):
    def on_get(self, req, resp):
        if req.cookies.get('X-AUTH-ID', None) == '1234567':
            with open('/tmp/remote_acess.txt', 'r') as f:
                resp.body = f.readlines()[-1]
        else:
            resp.body = "please login"
