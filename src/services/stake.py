from ..models import Stake as StakeModel
from ..common.db import init, save, find, destroy, count
from ..common.cache import cache, unmemoize


@cache.memoize(timeout=1000)
def count_stake():
    return count(StakeModel)


def find_stakes(**kwargs):
    return find(model=StakeModel, **kwargs)


def init_stake(**kwargs):
    return init(model=StakeModel, **kwargs)


def save_stake(stake):
    unmemoize(count_stake)
    return save(instance=stake)


def destroy_stake(stake):
    unmemoize(count_stake)
    return destroy(instance=stake)


def dump_stake(schema, stake, params=None):
    if params:
        for k, v in params.items():
            schema.context[k] = v
    return schema.dump(stake)


def clean_stake(schema, stake, **kwargs):
    return schema.load(stake, **kwargs)
