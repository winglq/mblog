from mblog.lib.basetemplate import BaseTemplate


class Index(BaseTemplate):
    template_name = "index.html"

    def on_get(self, req, resp):
        resp.content_type = 'text/html'
        resp.body = self.render(req, resp)
