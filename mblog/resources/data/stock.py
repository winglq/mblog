import json
import falcon

from mblog.db.api import stock_list
from mblog.db.api import stock_create
from mblog.db.api import stock_delete
from mblog.db.api import stock_update
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

    @falcon.before(authorize)
    def on_post(self, req, resp):
        req._parse_form_urlencoded()
        code = req.params['code']
        bid_price = req.params['bid_price']
        stop_loss_price = req.params['stop_loss_price']
        hold_position = req.params['hold_position']
        stock_create(req.context['user'].username, code, hold_position,
                     bid_price, stop_loss_price)
        raise falcon.HTTPFound(location='/user/stock')

    @falcon.before(authorize)
    def on_delete(self, req, resp):
        sid = req.query_string.split('=')[-1]
        stock_delete(sid)

    @falcon.before(authorize)
    def on_put(self, req, resp):
        req._parse_form_urlencoded()
        sid = req.params.pop('sid')
        stock_update(sid, **req.params)

    def get_rule(self, req):
        return "login"
