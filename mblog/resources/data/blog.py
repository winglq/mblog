import os
import json
import falcon

from mblog.datasources.file import FileSource


class Blog(object):
    def on_get(self, req, resp, entry_id):
        dvr= FileSource.get_instance()
        resp.body = json.dumps({'data': dvr.entry_to_html(entry_id)})
        resp.status = falcon.HTTP_200
