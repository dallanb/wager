from flask import g
from flask_restful import Resource
from http import HTTPStatus
from marshmallow import ValidationError
from ...common.error import ManualException
from ...services import Base as Service


class Base(Resource):
    def __init__(self):
        self.service = Service()
        self.logger = g.logger.getLogger(__name__)
        self.code = HTTPStatus

    def count(self, model):
        return self.service.count(model=model)

    def find(self, model, not_found=None, **kwargs):
        instance = self.service.find(model=model, **kwargs)
        if not instance.total and not_found:
            Base.throw_error(http_code=not_found)
        return instance

    def init(self, model, **kwargs):
        return self.service.init(model=model, **kwargs)

    def save(self, instance):
        return self.service.save(instance=instance)

    def destroy(self, instance):
        return self.service.destroy(instance=instance)

    def dump(self, schema, instance, params=None):
        return self.service.dump(schema=schema, instance=instance, params=params)

    def clean(self, schema, instance, **kwargs):
        try:
            return self.service.clean(schema=schema, instance=instance, **kwargs)
        except ValidationError as err:
            Base.throw_error(http_code=self.code.BAD_REQUEST, err=err.messages)

    def assign_attr(self, instance, attr):
        return self.service.assign_attr(instance=instance, attr=attr)

    def notify(self, topic, value, key):
        self.service.notify(topic=topic, value=value, key=key)

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
