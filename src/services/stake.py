from ..models import Stake as StakeModel
from ..common.db import init, save, find
from ..common.cache import cache, unmemoize


@cache.memoize(timeout=10)
def find_stake_by_uuid(uuid):
    return find(model=StakeModel, uuid=uuid, single=True)


def init_stake(**kwargs):
    return init(model=StakeModel, **kwargs)


def save_stake(stake):
    unmemoize(find_stake_by_uuid, uuid=stake.uuid)
    return save(instance=stake)
