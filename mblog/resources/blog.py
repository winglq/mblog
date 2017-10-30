from mblog.lib.basetemplate import BaseTemplate


class Blog(BaseTemplate):

    template_name = "blog.html"

    def on_get(self, req, resp, entry_id):
        resp.content_type = "text/html"
        resp.body = self.render(req, resp)
