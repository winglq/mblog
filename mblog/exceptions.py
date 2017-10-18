import falcon


class MBlogException(falcon.HTTPError):

    msg = ''
    error_code = 400

    def __init__(self, **kwargs):
        super(MBlogException, self).__init__(self.error_code)
        self.msg = self.msg.format(**kwargs)

    def to_dict(self, obj_type=dict):
        return {"error": self.msg, "status": self.status}

    def __str__(self):
        return self.msg


class InstanceNotInit(MBlogException):
    msg = "Intance of {class_name} not inited"


class DriverNotSupported(MBlogException):
    msg = "Driver {name} is not supported"


class RBDImportError(MBlogException):
    msg = "Import to {path} Error. Resaon: {reason}"


class RBDOperationError(MBlogException):
    msg = "CMD: '{cmd}' failed. Error Message: {msg}"


class ImageFormatError(MBlogException):
    msg = "Image format not supported"
