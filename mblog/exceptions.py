import falcon


class MBlogException(falcon.HTTPError):

    msg = ''
    error_code = 400

    def __init__(self, **kwargs):
        super(MBlogException, self).__init__(str(self.error_code))
        self.msg = self.msg.format(**kwargs)

    def to_dict(self, obj_type=dict):
        return {"error": self.msg, "status": self.status}

    def __str__(self):
        return self.msg

    def to_xml(self):
        return "<error><code>%s</code><message>%s</message></error>" % \
            (self.error_code, self.msg)


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


class UserNotExist(MBlogException):
    error_code = 403
    msg = "User {user} does not exist"


class PasswordInCorrect(MBlogException):
    error_code = 403
    msg = "Password does not match user name."


class TokenNotExist(MBlogException):
    error_code = 403
    msg = "Token expired or not exist"


class IllegalToken(MBlogException):
    error_code = 403
    msg = "Token is illegal"


class RequireLogin(MBlogException):
    error_code = 403
    msg = "Please login"


class Unauthorized(MBlogException):
    error_code = 403
    msg = "Unauthorized"
