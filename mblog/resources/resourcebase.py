class ReourceBase(object):
    def get_resource_id(self, req):
        path = req.path
        res_id = path.split('/')[-1]
        return res_id

    def get_owner(self, req=None):
        return None

    def get_rule(self, req=None):
        return None
