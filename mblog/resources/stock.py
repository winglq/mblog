from mblog.lib.basetemplate import BaseTemplate
from mblog.resources.resourcebase import ReourceBase


class Stock(BaseTemplate, ReourceBase):

    template_name = "stock.html"

    def on_get(self, req, resp):
        resp.content_type = "text/html"
        resp.body = self.render(req, resp)

