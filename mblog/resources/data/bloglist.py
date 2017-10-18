import json

from mblog.datasources.file import FileSource


class BlogList(object):
    def on_get(self, req, resp):
        filesource = FileSource.get_instance()
        resp.body = json.dumps(filesource.get_entries())
