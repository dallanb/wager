from ..models import Stake as StakeModel
from .. import cache
from .base import *


@cache.memoize(10)
def find_stake_by_uuid(uuid):
    if not uuid:
        return MissingParamError('uuid')
    if not is_uuid(uuid):
        raise InvalidTypeError('uuid', 'uuid')

    return find(model=StakeModel, uuid=uuid, single=True)


def init_stake(**kwargs):
    return init(model=StakeModel, **kwargs)


def save_stake(stake):
    return save(instance=stake)
