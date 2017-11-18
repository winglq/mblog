from mblog.lib.basetemplate import BaseTemplate
from mblog.resources.resourcebase import ResourceBase
from mblog.hooks.authorize import authorize


class UserStock(BaseTemplate, ResourceBase):

    template_name = "userstocks.html"

    def on_get(self, req, resp):
        resp.content_type = "text/html"
        resp.body = self.render(req, resp)

    def get_rule(self, req):
        return "owner"


class CreateUserStock(BaseTemplate, ResourceBase):
    template_name = "createuserstock.html"
    def on_get(self, req, resp):
        resp.content_type = "text/html"
        resp.body = self.render(req, resp)
