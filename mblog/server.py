import falcon
import os
import sys

if sys.version_info.major < 3:
    reload(sys)
    sys.setdefaultencoding('utf8')

from mblog.resources.index import Index
from mblog.resources.blog import Blog
from mblog.resources.data.blog import Blog as Dblog
from mblog.resources.data.bloglist import BlogList as DBlogList
from mblog.resources.data.image import Image
from mblog.resources.bloglist import BlogList
from mblog.resources.static import Static
from mblog.datasources.file import FileSource
from mblog.resources.stock import Stock
from mblog.resources.data.temperature import Temperature
from mblog.resources.data.host import Host
from mblog.resources.data.turtlesystem import TurtleSystem
from mblog.resources.login import Login
from mblog.resources.logout import Logout
from mblog.middlewares.authentication import AuthencationComponent
from mblog.resources.holiday import Holiday
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

    app = falcon.API(middleware=[AuthencationComponent()])
    app.resp_options.secure_cookies_by_default = False
    app.add_route('/', Index())
    app.add_route('/blogs/{entry_id}', Blog())
    app.add_route('/data/blogs/{entry_id}', Dblog())
    app.add_route('/statics/{name}', Static())
    app.add_route('/bloglist', BlogList())
    app.add_route('/data/bloglist', DBlogList())
    app.add_route('/data/temperature/{data:int}', Temperature())
    app.add_route('/data/temperature', Temperature())
    app.add_route('/data/images/{name}', Image())
    app.add_route('/login', Login())
    app.add_route('/logout', Logout())
    app.add_route('/data/server', Host())
    app.add_route('/data/tsystem/{sysnum:int}', TurtleSystem())
    app.add_route('/data/holiday/{date}', Holiday())
    app.add_route('/stock', Stock())
    return app
