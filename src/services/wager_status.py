from ..models import WagerStatus as WagerStatusModel
from ..common import WagerStatusEnum
from .base import *


def find_wager_status_by_enum(status_enum):
    if not status_enum:
        raise MissingParamError('status_enum')
    if not is_enum(status_enum, WagerStatusEnum):
        raise InvalidTypeError('status_enum', 'enum')
    return find(model=WagerStatusModel, name=status_enum, single=True)
