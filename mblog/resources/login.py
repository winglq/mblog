import falcon
import json

from mblog.lib.userauth import UserAuth


class Login(object):
    def on_post(self, req, resp):
        req._parse_form_urlencoded()
        user = req.params['user']
        pwd = req.params['password']
        token = UserAuth().authenticate(user, pwd)
        resp.set_cookie('X-AUTH-ID', token)
        resp.set_cookie('X-USER-ID', user)
        raise falcon.HTTPFound(location='/')
