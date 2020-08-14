from flask import g
from flask_restful import Resource
from http import HTTPStatus
from marshmallow import ValidationError
from ...common.error import ManualException
from ...services import Base as ServiceBase


class Base(Resource):
    def __init__(self):
        ServiceBase.__init__(self)
        self.logger = g.logger.getLogger(__name__)
        self.code = HTTPStatus

    # wrapper
    def find(self, model, not_found=None, **kwargs):
        instance = self.find(model=model, **kwargs)
        if not instance.total and not_found:
            Base.throw_error(http_code=not_found)
        return instance

    # wrapper
    def clean(self, schema, instance, **kwargs):
        try:
            return self.clean(schema=schema, instance=instance, **kwargs)
        except ValidationError as err:
            Base.throw_error(http_code=self.code.BAD_REQUEST, err=err.messages)

    @staticmethod
    def throw_error(http_code, **kwargs):
        if http_code is None:
            raise ManualException()
        code = http_code.value
        msg = kwargs.get('msg', http_code.phrase)
        err = kwargs.get('err', None)
        raise ManualException(code=code, msg=msg, err=err)

    @staticmethod
    def prepare_metadata(total_count, page_count, page, per_page):
        return {
            'total_count': total_count,
            'page_count': page_count,
            'page': page,
            'per_page': per_page
        }
