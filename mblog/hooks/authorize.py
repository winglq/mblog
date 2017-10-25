import falcon

from mblog.lib.user import User


def authorize(req, resp, resource, params):
    recvd_token = req.cookies.get('X-AUTH-ID', None)
    if recvd_token and User().authorize(token=recvd_token):
        return
    raise falcon.HTTPUnauthorized()
