from jinja2 import Environment, PackageLoader
from mblog.lib.navtemplate import NavTemplate

env = Environment(
    loader=PackageLoader('mblog', 'templates'))


class BaseTemplate(object):
    template_name = "__base.html"

    def __init__(self, included_templates=None):
        global env
        self.env = env
        self.included_templates = []
        if included_templates and not isinstance(included_templates, type([])):
            included_templates = [included_templates]
            self.included_templates.extend(included_templates)
        self.included_templates.append(NavTemplate())

    def get_render_params(self, req, resp):
        params = {}
        for temp in self.included_templates:
            temp_params = temp.get_render_params(req, resp)
            if temp_params:
                params.update(temp_params)
        return params

    def render(self, req, resp):
        template = env.get_template(self.template_name)
        all_params = self.get_render_params(req, resp)
        return template.render(all_params)
