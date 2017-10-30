import json

from mblog.lib.basetemplate import BaseTemplate
from mblog.datasources.file import FileSource
from mblog.lib.user import User


class BlogList(BaseTemplate):
    template_name = "__bloglist.html"

    def __init__(self):
        super(BlogList, self).__init__()
        self.included_templates = []

    def get_render_params(self, req, resp):
        params = super(BlogList, self).get_render_params(req, resp)
        user = req.context.get('user', None)
        filesource = FileSource.get_instance()
        entries = filesource.get_entries()
        updated_entries = []
        for entry in entries:
            acl = entry.get('acl', None)
            author = entry.get('author', None)
            if acl is None or acl[1] == '1' or author is None:
                updated_entries.append(entry)
                continue
            if acl[0] == '1':
                if user and author and User(author).group == user.group:
                    updated_entries.append(entry)
                continue
            if acl == '00':
                if user and author and author == user.username:
                    updated_entries.append(entry)
                continue

        params.update({'data': updated_entries})
        return params

    def on_get(self, req, resp):
        resp.body = json.dumps({'data': self.render(req, resp)})
