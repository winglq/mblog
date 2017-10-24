import os

from oslo_config import cfg
from mblog.stores.driver import StoreDriver
from mblog.stores import utils

filestore_drive_opts = [
    cfg.StrOpt('base_dir',
               help='The snapshots will be put in this directory',
               default='/var/lib/mblog/filestore')]

CONF = cfg.CONF

fg = cfg.OptGroup('filestore', 'filestore')
CONF.register_group(fg)
CONF.register_opts(filestore_drive_opts, fg)


class FilestoreDriver(StoreDriver):

    driver_prefix = 'file'
    CHUNCK_SIZE = 1024 * 1024 * 4

    def save(self, data, path):
        abs_path = os.path.join(CONF.filestore.base_dir, path)
        if not os.path.exists(CONF.filestore.base_dir):
            os.makedirs(CONF.filestore.base_dir)
        with open(abs_path, 'wb') as f:
            for d in utils.stream_iter(data, self.CHUNCK_SIZE):
                f.write(d)

    def load(self, path):
        return open(path, 'rb')
