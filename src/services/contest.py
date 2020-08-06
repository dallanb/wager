from ..models import Contest as ContestModel
from ..common.db import find, save, init, destroy, count
from ..common.cache import cache, unmemoize


@cache.memoize(timeout=1000)
def count_contest():
    return count(ContestModel)


def find_contest(**kwargs):
    return find(model=ContestModel, **kwargs)


def init_contest(**kwargs):
    return init(model=ContestModel, **kwargs)


def save_contest(contest):
    unmemoize(count_contest)
    return save(instance=contest)


def destroy_contest(contest):
    unmemoize(count_contest)
    return destroy(instance=contest)


def dump_contest(schema, contest, params=None):
    if params:
        for k, v in params.items():
            schema.context[k] = v
    return schema.dump(contest)


def clean_contest(schema, contest, **kwargs):
    return schema.load(contest, **kwargs)
