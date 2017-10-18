import falcon
import os

from mblog.resources.index import Index
from mblog.resources.blog import Blog
from mblog.resources.data.blog import Blog as Dblog
from mblog.resources.data.bloglist import BlogList as DBlogList
from mblog.resources.data.image import Image
from mblog.resources.bloglist import BlogList
from mblog.resources.static import Static
from mblog.datasources.file import FileSource
from mblog.resources.data.temperature import Temperature
from oslo_config import cfg
from oslo_log import log as logging


blog_path = os.path.join(os.getcwd(), 'mblog/markdowns')
site_path = os.path.join(os.getcwd(), 'mblog/site-mds')
FileSource([blog_path, site_path], ['about.md', 'contact.md', 'README.md'])


def launch(conf):
    logging.register_options(cfg.CONF)
    cfg.CONF(args=[],
             project='mblog')
    logging.setup(cfg.CONF, 'mblog')

    app = falcon.API()
    app.add_route('/', Index())
    app.add_route('/blogs/{entry_id}', Blog())
    app.add_route('/data/blogs/{entry_id}', Dblog())
    app.add_route('/statics/{name}', Static())
    app.add_route('/bloglist', BlogList())
    app.add_route('/data/bloglist', DBlogList())
    app.add_route('/data/temperature/{data:int}', Temperature())
    app.add_route('/data/temperature', Temperature())
    app.add_route('/data/images/{name}', Image())
    return app
