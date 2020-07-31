from flask import g
from functools import wraps
from flask_restful import Resource
from http import HTTPStatus
from ...common import ManualException


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
        err = kwargs.get('err', None)
        raise ManualException(code=code, msg=msg, err=err)

    @staticmethod
    def prepare_metadata(total, page, per_page):
        return {
            'total': total,
            'page': page,
            'per_page': per_page
        }
