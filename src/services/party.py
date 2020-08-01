from ..models import Party as PartyModel
from ..common.db import find, init, save
from ..common.cache import cache, unmemoize
from ..common.utils import generate_hash
from .party_member import init_party_member, save_party_member


@cache.memoize(timeout=1000)
def hash_members(members):
    return generate_hash(members)


@cache.memoize(timeout=10)
def find_party_by_hash(party_hash):
    return find(model=PartyModel, hash=party_hash, single=True)


def find_party_by_members(members):
    party_hash = hash_members(members=members)
    return find_party_by_hash(party_hash=party_hash)


@cache.memoize(timeout=10)
def find_party_by_uuid(uuid):
    return find(model=PartyModel, uuid=uuid, single=True)


def init_party(**kwargs):
    return init(model=PartyModel, **kwargs)


def init_party_by_members(members):
    party_hash = hash_members(members=members)
    party = init_party(hash=party_hash)
    for member in members:
        party_member = init_party_member(party=party, member=member)
        save_party_member(party_member=party_member)
    return party


def save_party(party):
    unmemoize(find_party_by_hash, hash=party.hash)
    unmemoize(find_party_by_uuid, uuid=party.uuid)
    return save(instance=party)
