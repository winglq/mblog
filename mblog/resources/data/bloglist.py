import os
import json


class BlogList(object):
    def on_get(self, req, resp):
        mds = os.listdir(os.path.join(os.getcwd(), 'mblog/markdowns'))
        resp.body = json.dumps({'titles': [x.split('.')[0] for x in mds if
                                           x.endswith('md')]})
