from ..models import Participant as ParticipantModel, ParticipantStatus as ParticipantStatusModel
from ..common.db import find, save, init, destroy, count, tablename
from ..common.cache import cache, unmemoize
from ..schemas import dump_participant_schema, dump_participants_schema


@cache.memoize(timeout=100)
def find_participant_status_by_enum(status_enum):
    return find(model=ParticipantStatusModel, name=status_enum, single=True)


@cache.memoize(timeout=1000)
def count_participant():
    return count(ParticipantModel)


def find_participant(**kwargs):
    return find(model=ParticipantModel, **kwargs)


# @cache.memoize(timeout=1000)
def find_participant_by_uuid(uuid):
    return find(model=ParticipantModel, uuid=uuid, single=True)


def init_participant(**kwargs):
    return init(model=ParticipantModel, **kwargs)


def save_participant(participant):
    # unmemoize(find_participant_by_uuid, uuid=participant.uuid)
    unmemoize(count_participant)
    return save(instance=participant)


def destroy_participant(participant):
    # unmemoize(find_participant_by_uuid, uuid=participant.uuid)
    unmemoize(count_participant)
    return destroy(instance=participant)


def dump_participant(participant, **kwargs):
    return dump_participant_schema.dump(participant, **kwargs)


def dump_participants(participants, **kwargs):
    return dump_participants_schema.dump(participants, **kwargs)
