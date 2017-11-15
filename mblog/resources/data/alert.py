import json
import Queue
import time
import threading
import StringIO

from mblog.tools.mail import send as sendmail
from mblog.lib.basetemplate import BaseTemplate
from mblog.lib.event import EventEngine, Event
from oslo_log import log as logging
from contextlib import contextmanager
from oslo_config import cfg

LOG = logging.getLogger(__name__)

stockalert_cfg = [
    cfg.IntOpt("mail_send_delay_time",
               help="After the handler receive the first alert, "
                    "the alert mail will send in mail_send_delay_time " 
                    "seconds. Alert with priority > 1 will send immediately.",
               default=120)]

CONF = cfg.CONF
CONF.register_opts(stockalert_cfg)

class StockAlertHandler(BaseTemplate):
    template_name = "alert_mail_template.html"

    def __init__(self):
        super(StockAlertHandler, self).__init__()
        self.included_templates = []
        self.alerts = []
        self.delay_send_started = False
        self.delay_time = CONF.mail_send_delay_time
        self.tables = []
        self.delay_send_thread = None
        self.max_hold_alert_count = 20

    def get_render_params(self, req, resp):
        return {'tables': self.tables}

    def delay_send_handle(self):
        if self.delay_send_started:
            return
        if len(self.alerts) == 0:
            return
        self.delay_send_started = True
        time.sleep(self.delay_time)
        self.send_alerts(self.alerts)
        self.alerts = []
        self.delay_send_started = False

    def __call__(self, alert):
        LOG.info("New stock alert priority %s" % alert['priority'])
        if int(alert['priority']) > 1:
            self.send_alerts([alert])
            return
        self.alerts.append(alert)
        if len(self.alerts) > self.max_hold_alert_count:
            self.send_alerts(self.alerts)
            self.alerts = []
            return
        if not self.delay_send_started:
            self.delay_send_thread = \
                threading.Thread(target=self.delay_send_handle)
            self.delay_send_thread.start()

    def send_alerts(self, alerts):
        alerts_dict = {}
        for alert in alerts:
            key = "%s %s" % (alert['data']['system'], alert['data']['action'])
            if alerts_dict.get(key, None) is None:
                alerts_dict[key] = []
            alerts_dict[key].extend(alert['data']['stocks'])
        tables = []
        for k, v  in alerts_dict.iteritems():
            tables.append({'title': k, 'table': self.stocks_to_html_table(v)})
        self.tables = tables
        subject = "Stock alert"
        message = self.render(None, None)
        sendmail(subject, message)

    @contextmanager
    def tag(self, ss, name):
        new_line = False
        if name in ['table', 'tr', 'tbody']:
            new_line = True
        append_line_end = False
        if name in ['tr']:
            append_line_end = True
        start_tag = "<%s>" % name + ("\n" if new_line else "")
        ss.write(start_tag)
        yield
        end_tag = ("\n" if append_line_end else "") + "</%s>" % name + \
            ("\n" if new_line else "")
        ss.write(end_tag)

    def stocks_to_html_table(self, stocks):
        sina_url = "http://finance.sina.com.cn/realstock/company/%s/nc.shtml"
        output = StringIO.StringIO()
        keys = ["break_time", "code", "name", "break_price",
                "previous_highest_price", "cv"]
        with self.tag(output, "table"):
            with self.tag(output, "tr"):
                for key in keys:
                    with self.tag(output, "th"):
                        output.write(key)
            with self.tag(output, "tbody"):
                for stock in stocks:
                    with self.tag(output, "tr"):
                        for key in keys:
                            with self.tag(output, "td"):
                                if key == "code":
                                    prefix = None
                                    if stock[key].startswith('60'):
                                        prefix = "SH"
                                    elif stock[key].startswith('00') or \
                                        stock[key].startswith('30'):
                                        prefix = "SZ"
                                    if prefix:
                                        ref = sina_url % (prefix + stock[key])
                                        output.write("<a href=%s>" % ref)
                                        output.write(stock[key])
                                        output.write("</a>")
                                        continue
                                output.write(stock[key])
        val = output.getvalue()
        output.close()
        return val


class Alert(object):

    EVENT_TYPE = 'alert'

    def __init__(self):
        self.event_engine = EventEngine.get_instance()
        self.stock_handler = StockAlertHandler()
        self.event_engine.register(self.EVENT_TYPE, self.distribute_alert)

    def on_post(self, req, resp):
        alert = json.loads(req.stream.read())
        event = Event(self.EVENT_TYPE, alert)
        self.event_engine.put(event)
        resp.body = "OK"

    def distribute_alert(self, event):
        alert = event.data
        if alert['type'] == 'stock':
            self.stock_handler(alert)
