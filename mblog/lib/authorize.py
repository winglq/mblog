import json
import os


class Authorize(object):
    policies = {}

    def __init__(self):
        path = '/tmp/policy.json'
        if os.path.exists(path):
            self.load(path)

    def load(self, path, force=False):
        if not self.policies or force:
            with open(path) as f:
                self.policies = json.loads(f.read())

    def authorize(self, user, resource, *args, **kwargs):
        if hasattr(resource, 'get_rule') and \
                resource.get_rule(*args, **kwargs):
            rule = resource.get_rule()
        else:
            rule = self.policies.get(type(resource).__name__, None)

        if not rule:
            return True

        if not hasattr(resource, 'get_owner'):
            return False

        if rule is "owner":
            return user.username == resource.get_owner(*args, **kwargs)
        if rule is "owner_or_group":
            if resource.get_owner().group() == user.group():
                return True
        return False
