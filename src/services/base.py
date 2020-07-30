from ..common.error import *
from ..common.cleaner import *
from ..common.db import *


def init(model, **kwargs):
    return model(**kwargs)


def count(model):
    return db.session.query(model).count()


def save(instance):
    if not instance:
        raise MissingParamError(instance.__tablename__)
    if not is_mapped(instance):
        raise InvalidTypeError(instance.__tablename__, 'mapped')

    if not is_pending(instance):
        db.session.add(instance)

    db.session.commit()
    return instance


def find(model, single=False, page=None, per_page=None, **kwargs):
    filters = []
    for k, v in kwargs.items():
        filters.append(('equal', [(k, v)]))

    instance = advanced_query(model=model, filters=filters, page=page, per_page=per_page, single=single)
    return instance


def destroy(instance):
    db.session.delete(instance)
    db.session.commit()
    return True
