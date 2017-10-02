import os
import json
import falcon

from mblog.datasources.file import FileSource


class Blog(object):
    def on_get(self, req, resp, entry_id):
        entries_dir = os.path.join(os.getcwd(), "mblog/markdowns")
        dvr = FileSource(entries_dir)
        resp.body = json.dumps({'data': dvr.entry_to_html(entry_id)})
        resp.status = falcon.HTTP_200
