import json
import requests

from mblog.lib.basetemplate import BaseTemplate


class BlogList(BaseTemplate):
    template_name = "__bloglist.html"

    def __init__(self):
        super(BlogList, self).__init__()
        self.included_templates = []

    def get_render_params(self, req, resp):
        params = super(BlogList, self).get_render_params(req, resp)
        entries = requests.get("http://127.0.0.1/data/bloglist")
        entries = json.loads(entries.text)
        params.update({'data': entries})
        return params

    def on_get(self, req, resp):
        resp.body = json.dumps({'data': self.render(req, resp)})
