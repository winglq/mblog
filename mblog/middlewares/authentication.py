from mblog.lib.userauth import UserAuth
from mblog import exceptions


class AuthencationComponent(object):
    def process_request(self, req, resp):
        token = req.cookies.get('X-AUTH-ID', None)
        usr = req.cookies.get('X-USER-ID', None)
        if token:
            token_usr = UserAuth().authenticate(token=token)
            if usr != token_usr:
                raise exceptions.IllegalToken()
        req.context['user'] = usr
