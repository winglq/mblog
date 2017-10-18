import os
import falcon

from oslo_config import cfg
from mblog.stores.driver import StoreDriver
from mblog import exceptions

CONF = cfg.CONF


class Image(object):
    def on_put(self, req, resp, name):
        if name.split('.')[-1] not in ['gif', 'jpg', 'png']:
            raise exceptions.ImageFormatError()
        drv = StoreDriver.factory("file")
        drv.save(req.stream, os.path.join(CONF.filestore.base_dir, name))
        resp.body = "OK"

    def on_get(self, req, resp, name):
        path = os.path.join(req.stream, CONF.filestore.base_dir, name)
        if not os.path.exists(path):
            raise falcon.HTTPNotFound(title="%s is not found" % name)
        with open(path, 'rb') as f:
            resp.body = f.read()
        if name.split('.')[-1] in ['gif', 'jpg', 'png']:
            resp.content_type = "image/%s" % (name.split('.')[-1])
        else:
            raise exceptions.ImageFormatError()
