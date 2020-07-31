from ..models import Party as PartyModel
from ..common.error import MissingParamError, InvalidTypeError
from ..common.cleaner import is_list, is_uuid, is_hash
from ..common.db import find, init, save
from ..common.cache import cache, unmemoize
from ..common.utils import generate_hash
from .party_member import init_party_member, save_party_member


@cache.memoize(timeout=1000)
def hash_members(members):
    if not members:
        raise MissingParamError('members')
    if not is_list(members):
        raise InvalidTypeError('members', 'list')

    return generate_hash(members)


@cache.memoize(timeout=10)
def find_party_by_hash(party_hash):
    if not party_hash:
        raise MissingParamError('party_hash')
    if not is_hash(party_hash):
        raise InvalidTypeError('party_hash', 'hash')

    return find(model=PartyModel, hash=party_hash, single=True)


def find_party_by_members(members):
    if not members:
        return MissingParamError('members')
    if not is_list(members):
        raise InvalidTypeError('members', 'list')

    # find hash for party
    party_hash = hash_members(members=members)
    return find_party_by_hash(party_hash=party_hash)


@cache.memoize(timeout=10)
def find_party_by_uuid(uuid):
    if not uuid:
        return MissingParamError('uuid')
    if not is_uuid(uuid):
        raise InvalidTypeError('uuid', 'uuid')

    return find(model=PartyModel, uuid=uuid, single=True)


def init_party(**kwargs):
    return init(model=PartyModel, **kwargs)


def init_party_by_members(members):
    if not members:
        raise MissingParamError('members')
    if not is_list(members):
        raise InvalidTypeError('members', 'list')

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
