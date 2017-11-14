import json
import os


class Holiday(object):
    def on_get(self, req, resp, date):
        date = date.replace('-', '')
        path = os.path.join(os.getcwd(), "mblog/files/holidays.json")
        with open(path) as f:
            holidays = json.load(f)
            if int(date) in holidays:
                resp.body = json.dumps(True)
            else:
                resp.body = json.dumps(False)

