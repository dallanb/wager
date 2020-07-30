import re
from .. import db


def advanced_query(model, filters=[], sort_by=None, limit=None, offset=None):
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

    return query.all()
