import falcon

from mblog.lib.userauth import UserAuth


def authorize(req, resp, resource, params):
    recvd_token = req.cookies.get('X-AUTH-ID', None)
    if recvd_token and UserAuth().authorize(token=recvd_token):
        return
    raise falcon.HTTPUnauthorized()
