import json
import os

from mblog import exceptions


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
        rule = None
        if hasattr(resource, 'get_rule'):
            rule = resource.get_rule(*args, **kwargs)
        if rule is None:
            if hasattr(resource, 'resource_name'):
                rule = self.policies.get(resource.resource_name, None)
            else:
                rule = self.policies.get(type(resource).__name__, None)

        if not rule:
            return True

        if not hasattr(resource, 'get_owner'):
            return False

        if not user:
            raise exceptions.RequireLogin()

        if rule is "login":
            return True

        if rule is "owner":
            return user.username == resource.get_owner(*args, **kwargs)
        if rule is "owner_or_group":
            if resource.get_owner().group() == user.group():
                return True
        return False
