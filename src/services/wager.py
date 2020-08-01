from ..models import Wager as WagerModel, WagerSchema
from ..common.db import find, save, init, destroy, count, tablename
from ..common.cache import cache, unmemoize
from .party import hash_members, find_party_by_hash, init_party_by_members, save_party
from .stake import init_stake, save_stake


def assign_wager_stake(currency=None, amount=None):
    stake = init_stake(currency=currency, amount=amount)
    return save_stake(stake=stake)


def assign_wager_party_by_members(members):
    party_hash = hash_members(members=members)
    party = find_party_by_hash(party_hash=party_hash)
    if party:
        return party
    party = init_party_by_members(members)
    return save_party(party)


def is_owner(wager, user):
    return wager.owner == user


@cache.memoize(timeout=1000)
def count_wager():
    return count(WagerModel)


def find_wager(**kwargs):
    return find(model=WagerModel, **kwargs)


@cache.memoize(timeout=1000)
def find_wager_by_uuid(uuid):
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
