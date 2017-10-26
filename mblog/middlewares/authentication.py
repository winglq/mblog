from mblog.lib.userauth import UserAuth
from mblog import exceptions


class AuthencationComponent(object):
    def process_request(self, req, resp):
        token = req.cookies.get('X-AUTH-ID', None)
        usr = req.cookies.get('X-USER-ID', None)
        if token:
            try:
                token_usr = UserAuth().authenticate(token=token)
            except exceptions.TokenNotExist:
                resp.unset_cookie('X-AUTH-ID')
                resp.unset_cookie('X-USER-ID')
                raise
            if usr != token_usr:
                raise exceptions.IllegalToken()
        req.context['user'] = usr
