import json

from mblog.lib.formaters.driver import Formater


class JsonFormater(Formater):
    def dumps(self, obj):
        return json.dumps(obj)

    def loads(self, s):
        return json.loads(s)
