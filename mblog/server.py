import falcon

from mblog.resources.index import Index
from mblog.resources.blog import Blog
from mblog.resources.data.blog import Blog as Dblog
from mblog.resources.data.bloglist import BlogList
from mblog.resources.static import Static


def launch(conf):
    app = falcon.API()
    app.add_route('/', Index())
    app.add_route('/blogs/{name}', Blog())
    app.add_route('/data/blogs/{name}', Dblog())
    app.add_route('/statics/{name}', Static())
    app.add_route('/data/bloglist', BlogList())
    return app

