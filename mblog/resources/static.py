import os
import falcon


class Static(object):
    def on_get(self, req, resp, name):
        path = os.path.join(os.getcwd(), "mblog/statics/%s" % name)
        with open(path, 'rb') as f:
            resp.body = f.read()
        if name.split('.')[-1] in ['gif', 'jpg', 'png']:
            resp.content_type = "image/%s" % (name.split('.')[-1])
