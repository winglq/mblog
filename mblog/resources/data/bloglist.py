import os
import json

from mblog.datasources.file import FileSource


class BlogList(object):
    def on_get(self, req, resp):
        dir_path = os.path.join(os.getcwd(), 'mblog/markdowns')
        filesource = FileSource(dir_path)
        resp.body = json.dumps(filesource.get_entries())
