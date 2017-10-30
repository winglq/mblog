import falcon

from mblog.lib.basetemplate import BaseTemplate
from mblog.resources.resourcebase import ReourceBase
from mblog.hooks.authorize import authorize
from mblog.datasources.file import FileSource


class Blog(BaseTemplate, ReourceBase):

    template_name = "blog.html"

    @falcon.before(authorize)
    def on_get(self, req, resp, entry_id):
        resp.content_type = "text/html"
        resp.body = self.render(req, resp)

    def get_owner(self, req):
        res_id = self.get_resource_id(req)
        entries = FileSource.get_instance().get_entries()
        for entry in entries:
            if entry['id'] == res_id:
                return entry['author']

    def get_rule(self, req):
        res_id = self.get_resource_id(req)
        entries = FileSource.get_instance().get_entries()
        acl = None
        for entry in entries:
            if entry['id'] == res_id:
                acl = entry.get('acl', None)
        if acl is None:
            return None
        # ACL[0] = group ACL[1] = everyone

        # Every one: X1
        if acl[1] == '1':
            return None

        # Group access: 10
        if acl[0] == '1':
            return 'owner_or_group'

        # owner only: 00
        return 'owner'
