import json
import falcon

from mblog.db.api import stock_list
from mblog.hooks.authorize import authorize
from mblog.resources.resourcebase import ResourceBase


class Stock(ResourceBase):

    @falcon.before(authorize)
    def on_get(self, req, resp):
        stocks = []
        user = req.context['user']
        for s in stock_list(user.username):
            dictret = dict(s.__dict__)
            dictret.pop('_sa_instance_state')
            stocks.append(dictret)
        resp.body = json.dumps(stocks)

    def get_rule(self, req):
        return "owner"

    def get_owner(self, req):
        return req.context["user"].username
