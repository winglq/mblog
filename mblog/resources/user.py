class User(object):
    def on_post(self, req, resp):
        if int(req.params['user']) + 9 == int(req.params['password']):
            resp.set_cookie("X-AUTH-ID", "1234567")
            resp.body = "LOG IN SUCCESS"
        else:
            resp.body = "FAIL"
