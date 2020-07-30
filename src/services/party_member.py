from ..models import PartyMember as PartyMemberModel
from .. import cache
from .base import *


@cache.memoize(10)
def find_party_member_by_uuid(uuid=None):
    if not uuid:
        return MissingParamError('uuid')
    if not is_uuid(uuid):
        raise InvalidTypeError('uuid', 'uuid')

    members = find(model=PartyMemberModel, uuid=uuid, single=True)
    return members


def init_party_member(**kwargs):
    return init(model=PartyMemberModel, **kwargs)


def save_party_member(party_member):
    return save(instance=party_member)
