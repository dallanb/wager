from ..models import Party as PartyModel, PartySchema
from ..common.db import find, init, save, destroy, count
from ..common.cache import cache, unmemoize


@cache.memoize(timeout=10)
def count_party():
    return count(PartyModel)


def find_party(**kwargs):
    return find(model=PartyModel, **kwargs)


@cache.memoize(timeout=10)
def find_party_by_uuid(uuid):
    return find(model=PartyModel, uuid=uuid, single=True)


def init_party(**kwargs):
    return init(model=PartyModel, **kwargs)


def save_party(party):
    unmemoize(find_party_by_uuid, uuid=party.uuid)
    unmemoize(count_party)
    return save(instance=party)


def destroy_party(party):
    unmemoize(find_party_by_uuid, uuid=party.uuid)
    unmemoize(count_party)
    return destroy(instance=party)


def dump_party(party, **kwargs):
    return PartySchema().dump(party, **kwargs)
