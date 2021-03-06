import falcon

from mblog import exceptions
from mblog.lib.userauth import UserAuth


def authorize(req, resp, resource, params):
    user = req.context.get("user", None)
    if not UserAuth().authorize(user, resource, req=req):
        raise falcon.HTTPUnauthorized()
