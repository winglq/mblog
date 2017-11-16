class ResourceBase(object):
    def get_resource_id(self, req):
        path = req.path
        res_id = path.split('/')[-1]
        return res_id

    def get_owner(self, req=None):
        if req.context.get("user", None) is None:
            return None
        return req.context["user"].username

    def get_rule(self, req=None):
        return None
