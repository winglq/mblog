import os


class Static(object):
    def on_get(self, req, resp, name):
        path = os.path.join(os.getcwd(), "mblog/statics/%s" % name)
        if os.path.exists(path):
            with open(path, 'rb') as f:
                resp.body = f.read()
            if name.split('.')[-1] in ['gif', 'jpg', 'png']:
                resp.content_type = "image/%s" % (name.split('.')[-1])
            if name.split('.')[-1] in ['css']:
                resp.content_type = "text/css"
            if name.split('.')[-1] in ['html']:
                resp.content_type = "text/html"
            if name.split('.')[-1] in ['js']:
                resp.content_type = "text/javascript"


        path = os.path.join(os.getcwd(), "mblog/markdowns/%s" % name)
        if os.path.exists(path):
            with open(path, 'rb') as f:
                resp.body = f.read()
            if name.split('.')[-1] in ['gif', 'jpg', 'png']:
                resp.content_type = "image/%s" % (name.split('.')[-1])
