from sqlalchemy import inspect
from src.common.error import *
from src.common.cleaner import *
from .. import db
import logging


def _query_builder(model, filters=[], expand=[], sort_by=None, limit=None, offset=None):
    query = db.session.query(model)
    for k, v in filters:
        if k == 'like':
            for like_k, like_v in v:
                search = "%{}%".format(like_v)
                query = query.filter(getattr(model, like_k).like(search))
        if k == 'equal':
            for equal_k, equal_v in v:
                query = query.filter(getattr(model, equal_k) == equal_v)
        if k == 'gt':
            for gt_k, gt_v in v:
                query = query.filter(getattr(model, gt_k) > gt_v)
        if k == 'gte':
            for gte_k, gte_v in v:
                query = query.filter(getattr(model, gte_k) >= gte_v)
        if k == 'lt':
            for lt_k, lt_v in v:
                query = query.filter(getattr(model, lt_k) < lt_v)
        if k == 'lte':
            for lte_k, lte_v in v:
                query = query.filter(getattr(model, lte_k) <= lte_v)
    for k in expand:
        tables = k.split('.')
        for i, table in enumerate(tables):
            if i == 0:
                query = query.join(getattr(model, table))
            else:
                nested_class = _get_class_by_tablename(tables[i - 1])
                query = query.join(getattr(nested_class, table))
    if sort_by is not None:
        direction = re.search('[.](a|de)sc', sort_by)
        if direction is not None:
            direction = direction.group()
        key = sort_by.split(direction)[0]
        if direction == '.asc':
            query = query.order_by(getattr(model, key).asc())
        elif direction == '.desc':
            query = query.order_by(getattr(model, key).desc())
        else:  # for now, lack of a direction will be interpreted as asc
            query = query.order_by(getattr(model, key).asc())
    if limit is not None:
        query = query.limit(limit)
    if offset is not None:
        query = query.offset(offset)
    logging.info(query)
    return query


def _get_class_by_tablename(tablename):
    for c in db.Model._decl_class_registry.values():
        if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
            return c


def _is_pending(instance):
    inspection = inspect(instance)
    return inspection.pending


def _get_cache_key(model, query):
    return f"{model.__tablename__}:{str(query)}"


def init(model, **kwargs):
    return model(**kwargs)


def count(model):
    return db.session.query(model).count()


def save(instance):
    if not instance:
        raise MissingParamError(instance.__tablename__)
    if not is_mapped(instance):
        raise InvalidTypeError(instance.__tablename__, 'mapped')

    if not _is_pending(instance):
        db.session.add(instance)

    db.session.commit()
    return instance


def find(model, single=False, page=None, per_page=None, expand=[], **kwargs):
    filters = []
    for k, v in kwargs.items():
        filters.append(('equal', [(k, v)]))

    query = _query_builder(model=model, filters=filters, expand=expand)

    if single:
        instance = query.first()
    elif page is not None and per_page is not None:
        instance = query.paginate(page, per_page, False).items
    else:
        instance = query.all()

    return instance


def destroy(instance):
    db.session.delete(instance)
    db.session.commit()
    return True


def tablename(model):
    return model.__tablename__
