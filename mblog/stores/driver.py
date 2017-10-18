from oslo_log import log as logging
from mblog import exceptions

LOG = logging.getLogger(__name__)


class StoreDriverMeta(type):
    def __init__(cls, name, bases, dct):
        if name != 'StoreDriver':
            if 'driver_prefix' not in dct or not dct['driver_prefix']:
                raise Exception("Need driver_prefix for class %s" % name)
            cls.supported_drivers[dct['driver_prefix']] = cls
        super(StoreDriverMeta, cls).__init__(name, bases, dct)


class StoreDriver(object):
    __metaclass__ = StoreDriverMeta

    inited_drivers = {}
    supported_drivers = {}
    driver_prefix = ''

    def save(self, data, path):
        '''
        save the data to path.
        parameters:
           @data: file like object which could be iterated.
           @path: destination location
        '''

        raise NotImplementedError

    @classmethod
    def factory(cls, prefix):
        if prefix not in cls.supported_drivers:
            # try to load the driver
            try:
                __import__("mblog.stores.%s.%s" % (prefix, prefix),
                           fromlist=['*'])
            except Exception as e:
                LOG.exception(e)
                raise exceptions.DriverNotSupported(name=prefix)
        if prefix not in cls.inited_drivers:
            cls.inited_drivers[prefix] = cls.supported_drivers[prefix]()
        return cls.inited_drivers[prefix]
