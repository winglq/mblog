import json


class Policy(object):
    def on_get(self, req, resp, policy):
        with open('/tmp/policies.json') as f:
            policies = json.load(f)
            resp_data = []
            for code, result in policies[policy]['result'].iteritems():
                result['code'] = code
                resp_data.append(result)
            resp.body = json.dumps(resp_data)

    def on_post(self, req, resp, policy):
        with open('/tmp/policies.json', 'w') as f:
            f.write(req.stream.read())
            resp.body = "OK"

class PolicyList(object):
    def on_get(self, req, resp):
        with open('/tmp/policies.json') as f:
            policies = json.load(f)
            resp.body = json.dumps([x for x in policies.keys()])
