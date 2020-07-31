from ..models import WagerStatus as WagerStatusModel
from ..common import WagerStatusEnum
from ..common.db import find
from ..common.cache import cache
from ..common.error import MissingParamError, InvalidTypeError
from ..common.cleaner import is_enum


@cache.memoize(timeout=100)
def find_wager_status_by_enum(status_enum):
    if not status_enum:
        raise MissingParamError('status_enum')
    if not is_enum(status_enum, WagerStatusEnum):
        raise InvalidTypeError('status_enum', 'enum')
    return find(model=WagerStatusModel, name=status_enum, single=True)
