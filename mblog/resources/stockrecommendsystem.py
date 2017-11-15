from mblog.lib.basetemplate import BaseTemplate
from mblog.resources.resourcebase import ResourceBase


class StockRecommendSystem(BaseTemplate, ResourceBase):

    template_name = "stock_recommend_system.html"

    def on_get(self, req, resp):
        resp.content_type = "text/html"
        resp.body = self.render(req, resp)
