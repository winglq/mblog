import falcon


class Logout(object):
    def on_get(self, req, resp):
        if req.context.get("user", None):
            resp.unset_cookie('X-AUTH-ID')
            resp.unset_cookie('X-USER-ID')
        raise falcon.HTTPFound(location='/')
