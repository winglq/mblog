import codecs
import markdown
import os
import json
import falcon


class Blog(object):
    def on_get(self, req, resp, name):
        md_name = name + ".md"
        md = os.path.join(os.getcwd(), "mblog/markdowns/%s" % md_name)
        with codecs.open(md, 'r', 'utf-8') as f:
            blog_content = markdown.markdown(
                f.read(),
                extensions=['markdown.extensions.tables',
                            'markdown.extensions.toc',
                            'markdown.extensions.nl2br',
                            'codehilite'])
        resp.body = json.dumps({'data': blog_content})
        resp.status = falcon.HTTP_200
