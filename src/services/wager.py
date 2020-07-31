from ..models import Wager as WagerModel, WagerSchema
from ..common.db import find, save, init, destroy, count, tablename
from ..common.cache import cache, unmemoize
from ..common.error import MissingParamError, InvalidTypeError, InvalidParamError
from ..common.cleaner import is_uuid, is_list
from .party import hash_members, find_party_by_hash, init_party_by_members, save_party
from .course import find_course_by_uuid
from .stake import init_stake, save_stake


def assign_wager_stake(currency=None, amount=None):
    stake = init_stake(currency=currency, amount=amount)
    return save_stake(stake=stake)


def assign_wager_course_by_uuid(uuid):
    if not uuid:
        return MissingParamError('uuid')
    if not is_uuid(uuid):
        raise InvalidTypeError('uuid', 'uuid')

    course = find_course_by_uuid(uuid=uuid)
    if not course:
        raise InvalidParamError('course')
    return course


def assign_wager_party_by_members(members):
    if not members:
        raise MissingParamError('members')
    if not is_list(members):
        raise InvalidTypeError('members', 'list')

    party_hash = hash_members(members=members)
    party = find_party_by_hash(party_hash=party_hash)
    if party:
        return party
    party = init_party_by_members(members)
    return save_party(party)


@cache.memoize(timeout=1000)
def count_wager():
    return count(WagerModel)


def find_wager(**kwargs):
    return find(model=WagerModel, **kwargs)


@cache.memoize(timeout=1000)
def find_wager_by_uuid(uuid):
    if not uuid:
        return MissingParamError('uuid')
    if not is_uuid(uuid):
        raise InvalidTypeError('uuid', 'uuid')

    return find(model=WagerModel, uuid=uuid, single=True)


def init_wager(**kwargs):
    return init(model=WagerModel, **kwargs)


def save_wager(wager):
    unmemoize(find_wager_by_uuid, uuid=wager.uuid)
    unmemoize(count_wager)
    return save(instance=wager)


def destroy_wager(wager):
    unmemoize(find_wager_by_uuid, uuid=wager.uuid)
    unmemoize(count_wager)
    return destroy(instance=wager)


def dump_wager(wager, **kwargs):
    return WagerSchema().dump(wager, **kwargs)
