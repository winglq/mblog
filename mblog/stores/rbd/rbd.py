import subprocess
import os

from datetime import datetime
from oslo_config import cfg
from oslo_log import log as logging
from mblog.stores.driver import StoreDriver
from mblog.stores import utils
from mblog.exceptions import RBDImportError, RBDOperationError

rbd_opts = [
    cfg.StrOpt('ceph_conf', default='/etc/ceph/ceph.conf',
               help='Ceph configuration file to use.'),
    cfg.StrOpt('ceph_user', default='cinder',
               help='The Ceph user to connect with.'),
]

CONF = cfg.CONF
rbd_grp = cfg.OptGroup('rbdstore', 'rbdstore')
CONF.register_group(rbd_grp)
CONF.register_opts(rbd_opts, rbd_grp)

LOG = logging.getLogger(__name__)


class RBDDriver(StoreDriver):

    driver_prefix = 'rbd'
    CHUNCK_SIZE = 1024 * 1024 * 4

    def save(self, data, path):
        pool, vol_snap = path.split('/')
        vol, snap = vol_snap.split('@')
        ceph_args = self._ceph_args(CONF.rbdstore.ceph_user,
                                    CONF.rbdstore.ceph_conf,
                                    pool)
        rbdcmd = ['rbd', 'import-diff'] + ceph_args
        rbdcmd.extend(['-', vol])
        LOG.debug("rbd command: %s" % ' '.join(rbdcmd))
        try:
            rbdp = subprocess.Popen(rbdcmd,
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            total = 0
            cur_t = datetime.now()
            for d in utils.stream_iter(data, self.CHUNCK_SIZE):
                rbdp.stdin.write(d)
                l = len(d)
                total += l
                LOG.debug("Written %s bytes to %s" % (l, path))
            delta = datetime.now() - cur_t
            stdout, stderr = rbdp.communicate()
            if rbdp.returncode:
                raise RBDOperationError(cmd=' '.join(rbdcmd),
                                        msg=stderr)
            LOG.info("Import to %s completed in %.2f seconds."
                     "Speed %.2f bytes/s" %
                     (path, delta.total_seconds(),
                      total / delta.total_seconds()))
        except RBDOperationError as e:
            LOG.exception(e)
            reason = os.strerror(rbdp.returncode) if \
                os.strerror(rbdp.returncode) else "Uknown Server Error"
            raise RBDImportError(path=path, reason=reason)
        except Exception as e:
            LOG.exception(e)
            reason = "Uknown Server Error"
            raise RBDImportError(path=path, reason=reason)

    def _ceph_args(self, user, conf=None, pool=None):
        """Create default ceph args for executing rbd commands.
        Copy from Openstack cinder ceph backup drvier.

        If no --conf is provided, rbd will look in the default locations e.g.
        /etc/ceph/ceph.conf
        """
        args = ['--id', user]
        if conf:
            args.extend(['--conf', conf])
        if pool:
            args.extend(['--pool', pool])

        return args
