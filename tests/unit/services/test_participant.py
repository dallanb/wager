import logging

from src import services, ManualException
from tests.helpers import generate_uuid

global_participant = None
global_stake = None
global_party = None
global_wager = None
participant_service = services.ParticipantService()


###########
# Find
###########
def test_participant_find_by_member_uuid(kafka_conn, reset_db, get_member_uuid, create_wager, create_party,
                                         create_participant):
    """
    GIVEN 1 participant instance in the database
    WHEN the find method is called with member_uuid
    THEN it should return 1 participant
    """
    global global_wager
    global global_party
    global global_participant
    member_uuid = get_member_uuid()
    global_wager = create_wager(contest_uuid=generate_uuid(), buy_in=5.0)
    global_party = create_party(wager_uuid=global_wager.uuid)
    _ = create_participant(party_uuid=global_party.uuid, member_uuid=member_uuid)

    participants = participant_service.find(member_uuid=member_uuid)

    assert participants.total == 1
    assert len(participants.items) == 1
    global_participant = participants.items[0]
    assert global_participant.member_uuid == member_uuid


def test_participant_find_by_uuid(kafka_conn):
    """
    GIVEN 1 participant instance in the database
    WHEN the find method is called with uuid
    THEN it should return 1 participant
    """
    global global_participant

    participants = participant_service.find(uuid=global_participant.uuid)

    assert participants.total == 1
    assert len(participants.items) == 1
    participant = participants.items[0]
    assert participant.uuid == global_participant.uuid


def test_participant_find_include_stakes(kafka_conn, create_stake):
    """
    GIVEN 1 participant instance in the database
    WHEN the find method is called with uuid and with include argument to also return stakes
    THEN it should return 1 participant
    """
    global global_participant
    global global_stake

    global_stake = create_stake(participant_uuid=global_participant.uuid)

    participants = participant_service.find(uuid=global_participant.uuid, include=['stakes'])

    assert participants.total == 1
    assert len(participants.items) == 1
    participant = participants.items[0]
    assert participant.stakes is not None
    assert len(participant.stakes) == 1
    assert participant.stakes[0].uuid == global_stake.uuid


def test_participant_find_expand_party(kafka_conn):
    """
    GIVEN 1 participant instance in the database
    WHEN the find method is called with uuid and with expand argument to also return party
    THEN it should return 1 participant
    """
    global global_participant
    global global_party

    participants = participant_service.find(uuid=global_participant.uuid, expand=['party'])

    assert participants.total == 1
    assert len(participants.items) == 1
    participant = participants.items[0]
    assert participant.party is not None
    assert participant.party.uuid == global_party.uuid
