import logging
from http import HTTPStatus

from ..common import Cache, DB, Event
from ..common.error import ManualException


class Base:
    def __init__(self):
        self.db = DB()
        # self.cache = Cache()
        self.event = Event()
        self.logger = logging.getLogger(__name__)

    # @cache.memoize(timeout=1000)
    def _count(self, model):
        return self.db.count(model=model)

    def _find(self, model, **kwargs):
        try:
            return self.db.find(model=model, **kwargs)
        except AttributeError:
            self.error(code=HTTPStatus.BAD_REQUEST)

    def _init(self, model, **kwargs):
        return self.db.init(model=model, **kwargs)

    def _add(self, instance):
        return self.db.add(instance=instance)

    def _commit(self):
        return self.db.commit()

    def _save(self, instance):
        return self.db.save(instance=instance)

    def _destroy(self, instance):
        return self.db.destroy(instance=instance)

    @classmethod
    def dump(cls, schema, instance, params=None):
        if params:
            for k, v in params.items():
                schema.context[k] = v
        return schema.dump(instance)

    @classmethod
    def clean(cls, schema, instance, **kwargs):
        return schema.load(instance, **kwargs)

    @staticmethod
    def assign_attr(instance, attr):
        for k, v in attr.items():
            instance.__setattr__(k, v)
        return instance

    def notify(self, topic, value, key):
        self.event.send(topic=topic, value=value, key=key)

    @staticmethod
    def error(code, **kwargs):
        if code is None:
            raise ManualException()
        error_code = code.value
        msg = kwargs.get('msg', code.phrase)
        err = kwargs.get('err', None)
        raise ManualException(code=error_code, msg=msg, err=err)
