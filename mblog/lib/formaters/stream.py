from mblog.lib.formaters.driver import Formater
from mblog.stores import utils


class StreamFormater(Formater):
    NAME = "STREAM"
    CHUNCK_SIZE = 1024 * 1024 * 4

    def dumps(self, s):
        yield utils.stream_iter(s, self.CHUNCK_SIZE)
