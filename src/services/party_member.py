from ..models import PartyMember as PartyMemberModel
from ..common.db import find, init, save
from ..common.cache import cache, unmemoize


@cache.memoize(timeout=10)
def find_party_member_by_uuid(uuid):
    members = find(model=PartyMemberModel, uuid=uuid, single=True)
    return members


def init_party_member(**kwargs):
    return init(model=PartyMemberModel, **kwargs)


def save_party_member(party_member):
    unmemoize(find_party_member_by_uuid, uuid=party_member.uuid)
    return save(instance=party_member)
