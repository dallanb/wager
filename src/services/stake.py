from ..models import Stake as StakeModel, StakeSchema
from ..common.db import init, save, find, destroy, count
from ..common.cache import cache, unmemoize


@cache.memoize(timeout=1000)
def count_stake():
    return count(StakeModel)


def find_stake(**kwargs):
    return find(model=StakeModel, **kwargs)


@cache.memoize(timeout=1000)
def find_stake_by_uuid(uuid):
    return find(model=StakeModel, uuid=uuid, single=True)


def init_stake(**kwargs):
    return init(model=StakeModel, **kwargs)


def save_stake(stake):
    unmemoize(find_stake_by_uuid, uuid=stake.uuid)
    unmemoize(count_stake)
    return save(instance=stake)


def destroy_stake(stake):
    unmemoize(find_stake_by_uuid, uuid=stake.uuid)
    unmemoize(count_stake)
    return destroy(instance=stake)


def dump_stake(stake, **kwargs):
    return StakeSchema().dump(stake, **kwargs)
