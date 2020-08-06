from ..models import Party as PartyModel
from ..common.db import find, init, save, destroy, count
from ..common.cache import cache, unmemoize


@cache.memoize(timeout=10)
def count_party():
    return count(PartyModel)


def find_parties(**kwargs):
    return find(model=PartyModel, **kwargs)


def init_party(**kwargs):
    return init(model=PartyModel, **kwargs)


def save_party(party):
    unmemoize(count_party)
    return save(instance=party)


def destroy_party(party):
    unmemoize(count_party)
    return destroy(instance=party)


def dump_party(schema, party, params=None):
    if params:
        for k, v in params.items():
            schema.context[k] = v
    return schema.dump(party)


def clean_party(schema, party, **kwargs):
    return schema.load(party, **kwargs)
