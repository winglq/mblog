class BaseException(Exception):
    msg = ""
    def __init__(self, **kwargs):
        self.message = self.msg % kwargs

class InstanceNotInit(BaseException):
    msg = "Intance of {class_name} not inited"
