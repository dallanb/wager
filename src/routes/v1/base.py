from flask import g
from functools import wraps
from flask_restful import Resource
from ...common import ManualException, Auth
from http import HTTPStatus


class Base(Resource):
    def __init__(self):
        self.logger = g.logger.getLogger(__name__)
        self.code = HTTPStatus

    @staticmethod
    def throw_error(http_code, **kwargs):
        if http_code is None:
            raise ManualException()
        code = http_code.value
        msg = kwargs.get('msg', http_code.phrase)
        raise ManualException(code=code, msg=msg)

    @staticmethod
    def check_user(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            Auth().check_user()
            return f(*args, **kwargs)

        wrap.__doc__ = f.__doc__
        wrap.__name__ = f.__name__
        return wrap
