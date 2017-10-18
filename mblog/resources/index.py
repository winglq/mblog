from jinja2 import Environment, PackageLoader

env = Environment(
    loader=PackageLoader('mblog', 'templates'))


class Index(object):
    def on_get(self, req, resp):
        template = env.get_template("index.html")
        resp.content_type = 'text/html'
        resp.body = template.render()
        
