from oslo_config import cfg
from datetime import datetime
from smtplib import SMTP, SMTP_SSL
email_cfg = [
    cfg.StrOpt('mailserver',
               help='mail server'),
    cfg.StrOpt('mailuser',
               help='login mail user'),
    cfg.StrOpt('mailpassword',
               help='login mail password'),
    cfg.ListOpt('receivers',
               help='mail send to'),
    cfg.StrOpt('use_ssl',
               help='use ssl',
               default=True)
]

CONF = cfg.CONF
CONF.register_opts(email_cfg)


def send(subject, body):
    message = ("From: %s\nTo: %s\nSubject: %s\n"
               "Date: %s\nContent-Type: text/html\n\n"
               "%s" % (CONF.mailuser, ",".join(CONF.receivers),
                       subject,
                       datetime.now().strftime("%Y-%m-%d %h:%M"),
                       body))
    if CONF.use_ssl:
        smtp = SMTP_SSL()
        smtp.connect(CONF.mailserver)
    else:
        smtp = SMTP()
        smtp.connect(CONF.mailserver)
    smtp.login(CONF.mailuser, CONF.mailpassword)
    smtp.sendmail(CONF.mailuser, CONF.receivers, message)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 7:
        print "usage: mail.py mailserver mailuser mailpassword receivers subject body"
        exit(1)
    CONF.use_ssl = True

    CONF.mailserver = sys.argv[1]
    CONF.mailuser = sys.argv[2]
    CONF.mailpassword = sys.argv[3]
    CONF.receivers = sys.argv[4]
    send(sys.argv[5], sys.argv[6])
