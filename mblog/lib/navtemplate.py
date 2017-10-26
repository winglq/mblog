class NavTemplate(object):
    def get_render_params(self, req, resp):
        if req.context.get("user", None):
            return {"user": req.context.get("user")}
