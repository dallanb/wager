import pytest

from src import services, ManualException
from tests.helpers import generate_uuid

stake_service = services.StakeService()


###########
# Find
###########
def test_stake_find(kafka_conn, reset_db, seed_wager, seed_party, seed_participant, seed_stake):
    """
    GIVEN 1 stake instance in the database
    WHEN the find method is called
    THEN it should return 1 stake
    """

    stakes = stake_service.find()
    assert stakes.total == 1
    assert len(stakes.items) == 1


def test_stake_find_by_uuid(kafka_conn):
    """
    GIVEN 1 stake instance in the database
    WHEN the find method is called with uuid
    THEN it should return 1 stake
    """

    stakes = stake_service.find(uuid=pytest.stake.uuid)
    assert stakes.total == 1
    assert len(stakes.items) == 1
    stake = stakes.items[0]
    assert stake.uuid == pytest.stake.uuid


def test_stake_find_by_participant_uuid(kafka_conn):
    """
    GIVEN 1 stake instance in the database
    WHEN the find method is called with participant_uuid
    THEN it should return 1 stake
    """

    stakes = stake_service.find(participant_uuid=pytest.participant.uuid)
    assert stakes.total == 1
    assert len(stakes.items) == 1
    stake = stakes.items[0]
    assert stake.participant.uuid == pytest.participant.uuid


def test_stake_find_expand_participant(kafka_conn):
    """
    GIVEN 1 stake instance in the database
    WHEN the find method is called with include argument to return participants
    THEN it should return 1 stake
    """

    stakes = stake_service.find(expand=['participant'])
    assert stakes.total == 1
    assert len(stakes.items) == 1
    stake = stakes.items[0]
    assert stake.participant.uuid == pytest.participant.uuid


def test_stake_find_w_pagination(kafka_conn, create_wager, create_party, create_participant, create_stake):
    """
    GIVEN 2 stake instance in the database
    WHEN the find method is called with valid pagination
    THEN it should return 1 stake
    """
    wager = create_wager(contest_uuid=generate_uuid(), buy_in=5.0)
    party = create_party(wager_uuid=wager.uuid)
    participant = create_participant(party_uuid=party.uuid, member_uuid=generate_uuid())
    _ = create_stake(participant_uuid=participant.uuid, amount=5.0)

    stakes_0 = stake_service.find(page=1, per_page=1)
    assert stakes_0.total == 2
    assert len(stakes_0.items) == 1

    stakes_1 = stake_service.find(page=2, per_page=1)
    assert stakes_1.total == 2
    assert len(stakes_1.items) == 1
    assert stakes_1.items[0] != stakes_0.items[0]

    stakes = stake_service.find(page=1, per_page=2)
    assert stakes.total == 2
    assert len(stakes.items) == 2


def test_stake_find_by_stake_uuid_w_bad_pagination(kafka_conn):
    """
    GIVEN 2 stake instance in the database
    WHEN the find method is called with out of range pagination
    THEN it should return 0 stake
    """
    stakes = stake_service.find(page=4, per_page=30)
    assert stakes.total == 2
    assert len(stakes.items) == 0


def test_stake_find_by_uuid_none_found(kafka_conn):
    """
    GIVEN 2 stake instance in the database
    WHEN the find method is called with random uuid
    THEN it should return 0 stake
    """
    stakes = stake_service.find(uuid=generate_uuid())
    assert stakes.total == 0
    assert len(stakes.items) == 0


def test_stake_find_by_non_existent_column(kafka_conn):
    """
    GIVEN 2 stake instance in the database
    WHEN the find method is called with random column
    THEN it should return 0 stake and ManualException with code 400
    """
    try:
        _ = stake_service.find(junk=generate_uuid())
    except ManualException as ex:
        assert ex.code == 400


def test_stake_find_by_non_existent_include(kafka_conn):
    """
    GIVEN 2 stake instance in the database
    WHEN the find method is called with include
    THEN it should return 0 stake and ManualException with code 400
    """

    try:
        _ = stake_service.find(include=['junk'])
    except ManualException as ex:
        assert ex.code == 400


def test_stake_find_by_non_existent_expand(kafka_conn):
    """
    GIVEN 2 stake instance in the database
    WHEN the find method is called with expand
    THEN it should return 0 stake and ManualException with code 400
    """

    try:
        _ = stake_service.find(expand=['junk'])
    except ManualException as ex:
        assert ex.code == 400


###########
# Create
###########
def test_stake_create(kafka_conn, reset_db, seed_wager, seed_party, seed_participant):
    """
    GIVEN 0 stake instance in the database
    WHEN the create method is called
    THEN it should return 1 stake and add 1 stake instance into the database
    """
    stake = stake_service.create(participant=pytest.participant, amount=5.0)
    assert stake.uuid is not None
    assert stake.participant is not None


def test_stake_create_dup_participant(kafka_conn):
    """
    GIVEN 1 stake instance in the database
    WHEN the create method is called with duplicate participant
    THEN it should return 0 stake and add 0 stake instance into the database and ManualException with code 500
    """

    try:
        _ = stake_service.create(participant=pytest.participant, amount=5.0)
    except ManualException as ex:
        assert ex.code == 500


def test_stake_create_w_participant_uuid(kafka_conn, reset_db, seed_wager, seed_party, seed_participant):
    """
    GIVEN 0 stake instance in the database
    WHEN the create method is called with participant_uuid
    THEN it should return 1 stake and add 1 stake instance into the database
    """
    stake = stake_service.create(participant_uuid=pytest.participant.uuid, amount=5.0)
    assert stake.uuid is not None


def test_stake_create_wo_participant(kafka_conn):
    """
    GIVEN 1 stake instance in the database
    WHEN the create method is called without participant
    THEN it should return 0 stake and add 0 stake instance into the database and ManualException with code 500
    """

    try:
        _ = stake_service.create(amount=5.0)
    except ManualException as ex:
        assert ex.code == 500


def test_stake_create_w_non_existent_participant_uuid(kafka_conn):
    """
    GIVEN 1 stake instance in the database
    WHEN the create method is called with non existent participant uuid
    THEN it should return 0 stake and add 0 stake instance into the database and ManualException with code 500
    """

    try:
        _ = stake_service.create(participant_uuid=generate_uuid(), amount=5.0)
    except ManualException as ex:
        assert ex.code == 500


def test_stake_create_w_bad_amount(kafka_conn, reset_db, seed_wager, seed_party, seed_participant):
    """
    GIVEN 1 stake instance in the database
    WHEN the create method is called with invalid amount
    THEN it should return 0 stake and add 0 stake instance into the database and ManualException with code 500
    """

    try:
        _ = stake_service.create(participant=pytest.participant, amount='five')
    except ManualException as ex:
        assert ex.code == 500


def test_stake_create_wo_amount(kafka_conn):
    """
    GIVEN 0 stake instance in the database
    WHEN the create method is called without amount
    THEN it should return 1 stake and add 1 stake instance into the database
    """

    stake = stake_service.create(participant=pytest.participant)
    assert stake.amount == 0.0


def test_stake_create_w_bad_field(kafka_conn, reset_db, seed_wager, seed_party, seed_participant):
    """
    GIVEN 0 stake instance in the database
    WHEN the create method is called with a non existent field
    THEN it should return 0 stake and add 0 stake instance into the database and ManualException with code 500
    """

    participants = services.ParticipantService().find()
    participant = participants.items[0]
    try:
        _ = stake_service.create(participant=participant, amount=5.0, junk='junk')
    except ManualException as ex:
        assert ex.code == 500
