from flask import g, request
from functools import wraps
from .error import ManualException


def check_user(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        g.user = request.headers.get('X-Consumer-Custom-ID')
        if not g.user:
            raise ManualException(code=400, msg='Missing user data')
        return f(*args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
