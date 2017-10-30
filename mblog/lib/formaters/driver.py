class Formater(object):
    def dumps(self, obj):
        raise NotImplementedError

    def loads(self, s):
        raise NotImplementedError

    def convert_to(self, to):
        raise NotImplementedError
