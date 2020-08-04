from ..models import Wager as WagerModel, WagerSchema
from ..common.db import find, save, init, destroy, count, tablename
from ..common.cache import cache, unmemoize


@cache.memoize(timeout=1000)
def count_wager():
    return count(WagerModel)


def find_wager(**kwargs):
    return find(model=WagerModel, **kwargs)


@cache.memoize(timeout=1000)
def find_wager_by_uuid(uuid):
    return find(model=WagerModel, uuid=uuid, single=True)


def init_wager(**kwargs):
    return init(model=WagerModel, **kwargs)


def save_wager(wager):
    unmemoize(find_wager_by_uuid, uuid=wager.uuid)
    unmemoize(count_wager)
    return save(instance=wager)


def destroy_wager(wager):
    unmemoize(find_wager_by_uuid, uuid=wager.uuid)
    unmemoize(count_wager)
    return destroy(instance=wager)


def dump_wager(wager, **kwargs):
    return WagerSchema().dump(wager, **kwargs)
