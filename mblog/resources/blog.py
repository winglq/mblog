from jinja2 import Environment, PackageLoader

env = Environment(
        loader=PackageLoader('mblog', 'templates'))

class Blog(object):
    def on_get(self, req, resp, entry_id):
        template = env.get_template("blog.html")
        resp.content_type = 'text/html'
        resp.body = template.render()
