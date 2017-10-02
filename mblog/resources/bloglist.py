import json
import requests

from jinja2 import Environment, PackageLoader

env = Environment(
        loader=PackageLoader('mblog', 'templates'))


class BlogList(object):
    def on_get(self, req, resp):
        entries = requests.get("http://127.0.0.1/data/bloglist")
        entries = json.loads(entries.text)
        template = env.get_template("__bloglist.html")
        resp.body = json.dumps({'data': template.render({'data': entries})})
