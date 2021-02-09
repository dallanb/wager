from src import services, ManualException
from tests.helpers import generate_uuid

contest = None
wager = None


###########
# Find
###########
def test_contest_find_by_contest_uuid(reset_db, get_contest_uuid, create_wager):
    """
    GIVEN 1 contest instance in the database
    WHEN the find method is called with contest_uuid
    THEN it should return 1 contest
    """
    contest_uuid = get_contest_uuid()
    _ = create_wager(contest_uuid=contest_uuid, buy_in=5.0)
    contest_service = services.ContestService()

    global contest
    contests = contest_service.find(contest_uuid=contest_uuid)
    assert contests.total == 1
    assert len(contests.items) == 1
    contest = contests.items[0]
    assert contest.contest_uuid == contest_uuid


def test_contest_find_by_uuid():
    """
    GIVEN 1 contest instance in the database
    WHEN the find method is called with uuid
    THEN it should return 1 contest
    """
    contest_service = services.ContestService()

    global contest
    contests = contest_service.find(uuid=contest.uuid)
    assert contests.total == 1
    assert len(contests.items) == 1
    contest = contests.items[0]
    assert contest.uuid == contest.uuid


def test_contest_find_include_wager():
    """
    GIVEN 1 contest instance in the database
    WHEN the find method is called with uuid with include argument to also return wager
    THEN it should return 1 contest
    """
    contest_service = services.ContestService()

    global contest
    global wager
    contests = contest_service.find(uuid=contest.uuid, include=['wager'])
    assert contests.total == 1
    assert len(contests.items) == 1
    contest = contests.items[0]
    assert contest.wager.uuid is not None
    wager = contest.wager


def test_contest_find_by_wager_uuid():
    """
    GIVEN 1 contest instance in the database
    WHEN the find method is called with wager_uuid
    THEN it should return 1 contest
    """
    contest_service = services.ContestService()

    global contest
    global wager
    contests = contest_service.find(wager_uuid=wager.uuid)
    assert contests.total == 1
    assert len(contests.items) == 1
    contest = contests.items[0]
    assert contest.wager.uuid == wager.uuid


def test_contest_find_by_contest_uuid_multiple(get_contest_uuid, create_wager):
    """
    GIVEN 2 contest instance in the database
    WHEN the find method is called with contest_uuid
    THEN it should return 2 contest
    """
    contest_uuid = get_contest_uuid()
    _ = create_wager(contest_uuid=contest_uuid, buy_in=5.0)
    contest_service = services.ContestService()

    global contest
    contests = contest_service.find(contest_uuid=contest_uuid)
    assert contests.total == 2
    assert len(contests.items) == 2


def test_contest_find_by_contest_uuid_multiple_match_single(reset_db, get_contest_uuid, create_wager):
    """
    GIVEN 2 contest instance in the database
    WHEN the find method is called with contest_uuid
    THEN it should return 1 contest
    """
    contest_uuid = get_contest_uuid()
    _ = create_wager(contest_uuid=contest_uuid, buy_in=5.0)
    _ = create_wager(contest_uuid=generate_uuid(), buy_in=5.0)
    contest_service = services.ContestService()

    contests = contest_service.find(contest_uuid=contest_uuid)
    assert contests.total == 1
    assert len(contests.items) == 1


def test_contest_find_by_contest_uuid_none_found(reset_db, get_contest_uuid):
    """
    GIVEN 0 contest instance in the database
    WHEN the find method is called with contest_uuid
    THEN it should return 0 contest
    """
    contest_uuid = get_contest_uuid()
    contest_service = services.ContestService()

    contests = contest_service.find(contest_uuid=contest_uuid)
    assert contests.total == 0
    assert len(contests.items) == 0


def test_contest_find_by_non_existent_column(reset_db, get_contest_uuid, create_wager):
    """
    GIVEN 1 contest instance in the database
    WHEN the find method is called with contest_uuid
    THEN it should return 1 contest
    """
    contest_uuid = get_contest_uuid()
    _ = create_wager(contest_uuid=contest_uuid, buy_in=5.0)
    contest_service = services.ContestService()

    try:
        _ = contest_service.find(junk=contest_uuid)
    except ManualException as ex:
        assert ex.code == 400


def test_contest_find_by_non_existent_include(get_contest_uuid, create_wager):
    """
    GIVEN 0 contest instance in the database
    WHEN the find method is called with include
    THEN it should return 0 contest
    """
    contest_service = services.ContestService()

    try:
        _ = contest_service.find(include=['junk'])
    except ManualException as ex:
        assert ex.code == 400


def test_contest_find_by_non_existent_expand(get_contest_uuid, create_wager):
    """
    GIVEN 0 contest instance in the database
    WHEN the find method is called with expand
    THEN it should return 0 contest
    """
    contest_service = services.ContestService()

    try:
        _ = contest_service.find(expand=['junk'])
    except ManualException as ex:
        assert ex.code == 400
