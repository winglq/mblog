import json
from mblog.tools.mail import send as sendmail
from mblog.lib.basetemplate import BaseTemplate


class AlertMailHandler(BaseTemplate):
    template_name = "alert_mail_template.html"

    def __init__(self):
        super(AlertMailHandler, self).__init__()
        self.included_templates = []
        self.stocks = None

    def get_render_params(self, req, resp):
        return {'stocks': self.stocks, 'info': self.info}

    def handle(self, alert):
        if alert['type'] == 'buy':
            subject = "Buy Alert"
        elif alert['type'] == 'sell':
            subject = "Sell Alert"

        self.stocks = alert['stocks']
        self.info = alert['info']
        message = self.render(None, None)
        sendmail(subject, message)


class Alert(object):
    def __init__(self):
        self.handlers = [AlertMailHandler()]
    def on_post(self, req, resp):
        alert = json.loads(req.stream.read())
        for handle in self.handlers:
            handle.handle(alert)
        resp.body = "OK"

