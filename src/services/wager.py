from ..models import Wager as WagerModel
from ..common.db import find, save, init, destroy, count
from ..common.cache import cache, unmemoize


@cache.memoize(timeout=1000)
def count_wager():
    return count(WagerModel)


def find_wagers(**kwargs):
    return find(model=WagerModel, **kwargs)


def init_wager(**kwargs):
    return init(model=WagerModel, **kwargs)


def save_wager(wager):
    unmemoize(count_wager)
    return save(instance=wager)


def destroy_wager(wager):
    unmemoize(count_wager)
    return destroy(instance=wager)


def dump_wager(schema, wager, params=None):
    if params:
        for k, v in params.items():
            schema.context[k] = v
    return schema.dump(wager)


def clean_wager(schema, wager, **kwargs):
    return schema.load(wager, **kwargs)
