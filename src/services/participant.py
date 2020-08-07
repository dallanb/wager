from ..models import Participant as ParticipantModel
from ..common.db import find, save, init, destroy, count
from ..common.cache import cache, unmemoize


@cache.memoize(timeout=1000)
def count_participant():
    return count(ParticipantModel)


def find_participants(**kwargs):
    return find(model=ParticipantModel, **kwargs)


def init_participant(**kwargs):
    return init(model=ParticipantModel, **kwargs)


def save_participant(participant):
    unmemoize(count_participant)
    return save(instance=participant)


def destroy_participant(participant):
    unmemoize(count_participant)
    return destroy(instance=participant)


def dump_participant(schema, participant, params=None):
    if params:
        for k, v in params.items():
            schema.context[k] = v
    return schema.dump(participant)


def clean_participant(schema, participant, **kwargs):
    return schema.load(participant, **kwargs)
