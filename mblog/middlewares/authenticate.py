import falcon

from mblog.lib.userauth import UserAuth


class AuthenticateMiddleware(object):
    def __init__(self, app, conf):
        self.app = app
        self.conf = conf

    def get_resp_headers(self, token=None):
        headers = [("Content-type", "text/json")]
        if token:
            headers.append(("Set-Cookie", "X-AUTH-ID=%s" % token))
        return headers

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith('/login'):
            user = environ['wsgi.input'].read()
            usr = user.split('&')[0].split('=')[-1]
            pwd = user.split('&')[1].split('=')[-1]
            try:
                token = UserAuth().authenticate(usr, pwd)
            except falcon.HTTPError as e:
                start_response(str(e.status), self.get_resp_headers())
                return str(e)

            if '?next=' in environ['PATH_INFO']:
                environ['PATH_INFO'] = environ['PATH_INFO']. \
                    split('?next=')[-1]
                environ['HTTP_COOKIE'] += '; X-AUTH-ID=%s' % token
                resp = self.app(environ, start_response)
                return resp
            else:
                start_response('200', self.get_resp_headers(token))
                return "Login successful"
        else:
            resp = self.app(environ, start_response)
            return resp


def factory(global_conf, **local_conf):
    def producer(app):
        conf = global_conf.copy()
        conf.update(local_conf)
        return AuthenticateMiddleware(app, conf)
    return producer
