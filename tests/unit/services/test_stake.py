from src import services, ManualException
from tests.helpers import generate_uuid

global_stake = None
global_participant = None
stake_service = services.StakeService()


###########
# Find
###########
def test_stake_find(kafka_conn, reset_db, seed_stake):
    """
    GIVEN 1 stake instance in the database
    WHEN the find method is called
    THEN it should return 1 stake
    """

    global global_stake
    global global_participant

    stakes = stake_service.find()
    assert stakes.total == 1
    assert len(stakes.items) == 1
    global_stake = stakes.items[0]
    global_participant = stakes.items[0].participant


def test_stake_find_by_uuid(kafka_conn):
    """
    GIVEN 1 stake instance in the database
    WHEN the find method is called with uuid
    THEN it should return 1 stake
    """
    global global_stake
    stakes = stake_service.find(uuid=global_stake.uuid)
    assert stakes.total == 1
    assert len(stakes.items) == 1
    stake = stakes.items[0]
    assert stake.uuid == global_stake.uuid


def test_stake_find_by_participant_uuid(kafka_conn):
    """
    GIVEN 1 stake instance in the database
    WHEN the find method is called with participant_uuid
    THEN it should return 1 stake
    """

    global global_stake
    global global_participant

    stakes = stake_service.find(participant_uuid=global_participant.uuid)
    assert stakes.total == 1
    assert len(stakes.items) == 1
    stake = stakes.items[0]
    assert stake.participant.uuid == global_participant.uuid


def test_stake_find_include_participants(kafka_conn):
    """
    GIVEN 1 stake instance in the database
    WHEN the find method is called with include argument to return participants
    THEN it should return 1 stake
    """

    global global_stake
    global global_participant

    stakes = stake_service.find(include=['participants'])
    assert stakes.total == 1
    assert len(stakes.items) == 1
    stake = stakes.items[0]
    assert stake.participant.uuid == global_participant.uuid


def test_stake_find_w_pagination(kafka_conn, seed_stake):
    """
    GIVEN 2 stake instance in the database
    WHEN the find method is called with valid pagination
    THEN it should return 1 stake
    """
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
