from src import services, ManualException
from tests.helpers import generate_uuid

global_contest = None
global_wager = None
contest_service = services.ContestService()


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

    global global_contest
    contests = contest_service.find(contest_uuid=contest_uuid)
    assert contests.total == 1
    assert len(contests.items) == 1
    global_contest = contests.items[0]
    assert global_contest.contest_uuid == contest_uuid


def test_contest_find_by_uuid():
    """
    GIVEN 1 contest instance in the database
    WHEN the find method is called with uuid
    THEN it should return 1 contest
    """

    global global_contest
    contests = contest_service.find(uuid=global_contest.uuid)
    assert contests.total == 1
    assert len(contests.items) == 1
    contest = contests.items[0]
    assert contest.uuid == global_contest.uuid


def test_contest_find_include_wager():
    """
    GIVEN 1 contest instance in the database
    WHEN the find method is called with uuid with include argument to also return wager
    THEN it should return 1 contest
    """

    global global_contest
    global global_wager
    contests = contest_service.find(uuid=global_contest.uuid, include=['wager'])
    assert contests.total == 1
    assert len(contests.items) == 1
    contest = contests.items[0]
    assert contest.wager.uuid is not None
    global_wager = contest.wager


def test_contest_find_by_wager_uuid():
    """
    GIVEN 1 contest instance in the database
    WHEN the find method is called with wager_uuid
    THEN it should return 1 contest
    """

    global global_contest
    global global_wager
    contests = contest_service.find(wager_uuid=global_wager.uuid)
    assert contests.total == 1
    assert len(contests.items) == 1
    contest = contests.items[0]
    assert contest.wager.uuid == global_wager.uuid


def test_contest_find_by_contest_uuid_multiple(get_contest_uuid, create_wager):
    """
    GIVEN 2 contest instance in the database
    WHEN the find method is called with contest_uuid
    THEN it should return 2 contest
    """
    contest_uuid = get_contest_uuid()
    _ = create_wager(contest_uuid=contest_uuid, buy_in=5.0)

    global global_contest
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

    contests = contest_service.find(contest_uuid=contest_uuid)
    assert contests.total == 1
    assert len(contests.items) == 1


def test_contest_find_by_contest_uuid_w_pagination(get_contest_uuid):
    """
    GIVEN 2 contest instance in the database
    WHEN the find method is called with contest_uuid and valid pagination
    THEN it should return 1 contest
    """
    contest_uuid = get_contest_uuid()

    contests = contest_service.find(contest_uuid=contest_uuid, page=1, per_page=1)
    assert contests.total == 1
    assert len(contests.items) == 1
    assert contests.items[0].contest_uuid == contest_uuid


def test_contest_find_by_contest_uuid_w_bad_pagination(get_contest_uuid):
    """
    GIVEN 2 contest instance in the database
    WHEN the find method is called with contest_uuid and out of range pagination
    THEN it should return 0 contest
    """
    contest_uuid = get_contest_uuid()

    contests = contest_service.find(contest_uuid=contest_uuid, page=4, per_page=30)
    assert contests.total == 1
    assert len(contests.items) == 0


def test_contest_find_by_contest_uuid_none_found(reset_db, get_contest_uuid):
    """
    GIVEN 0 contest instance in the database
    WHEN the find method is called with contest_uuid
    THEN it should return 0 contest
    """
    contest_uuid = get_contest_uuid()

    contests = contest_service.find(contest_uuid=contest_uuid)
    assert contests.total == 0
    assert len(contests.items) == 0


def test_contest_find_by_non_existent_column(reset_db, get_contest_uuid, create_wager):
    """
    GIVEN 1 contest instance in the database
    WHEN the find method is called with contest_uuid
    THEN it should return 0 contest and ManualException with code 400
    """
    contest_uuid = get_contest_uuid()
    _ = create_wager(contest_uuid=contest_uuid, buy_in=5.0)

    try:
        _ = contest_service.find(junk=contest_uuid)
    except ManualException as ex:
        assert ex.code == 400


def test_contest_find_by_non_existent_include(get_contest_uuid, create_wager):
    """
    GIVEN 0 contest instance in the database
    WHEN the find method is called with include
    THEN it should return 0 contest and ManualException with code 400
    """

    try:
        _ = contest_service.find(include=['junk'])
    except ManualException as ex:
        assert ex.code == 400


def test_contest_find_by_non_existent_expand(get_contest_uuid, create_wager):
    """
    GIVEN 0 contest instance in the database
    WHEN the find method is called with expand
    THEN it should return 0 contest and ManualException with code 400
    """

    try:
        _ = contest_service.find(expand=['junk'])
    except ManualException as ex:
        assert ex.code == 400


###########
# Create
###########
def test_contest_create(reset_db, get_contest_uuid):
    """
    GIVEN 0 contest instance in the database
    WHEN the create method is called
    THEN it should return 1 contest and add 1 contest instance into the database
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    contest_uuid = get_contest_uuid()
    contest = contest_service.create(contest_uuid=contest_uuid, buy_in=5.0, wager=global_wager)
    assert contest.uuid is not None
    assert contest.contest_uuid == contest_uuid
    assert contest.buy_in == 5.0

    contests = contest_service.find(contest_uuid=contest_uuid)
    assert contests.total == 1
    assert len(contests.items) == 1


def test_contest_create_dup_contest_uuid(get_contest_uuid):
    """
    GIVEN 1 contest instance in the database
    WHEN the create method is called with contest_uuid of contest already in the database
    THEN it should return 1 contest and add 1 contest instance into the database
    """
    wager = services.WagerService().create(status='active')
    contest_uuid = get_contest_uuid()
    contest = contest_service.create(contest_uuid=contest_uuid, buy_in=1.0, wager=wager)
    assert contest.uuid is not None
    assert contest.contest_uuid == contest_uuid
    assert contest.buy_in == 1.0

    contests = contest_service.find(contest_uuid=contest_uuid)
    assert contests.total == 2
    assert len(contests.items) == 2


def test_contest_create_dup_wager(get_contest_uuid):
    """
    GIVEN 2 contest instance in the database
    WHEN the create method is called with wager of contest already in the database
    THEN it should return 1 contest and add 1 contest instance into the database
    """
    global global_wager
    contest_uuid = generate_uuid()
    contest = contest_service.create(contest_uuid=contest_uuid, buy_in=4.0, wager=global_wager)
    assert contest.uuid is not None
    assert contest.contest_uuid == contest_uuid
    assert contest.buy_in == 4.0

    contests = contest_service.find(contest_uuid=contest_uuid)
    assert contests.total == 1
    assert len(contests.items) == 1

    contests = contest_service.find(wager_uuid=global_wager.uuid)
    assert contests.total == 2
    assert len(contests.items) == 2


def test_contest_create_int_buy_in(reset_db, get_contest_uuid):
    """
    GIVEN 0 contest instance in the database
    WHEN the create method is called with integer buy in
    THEN it should return 1 contest and add 1 contest instance into the database
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    contest_uuid = get_contest_uuid()
    contest = contest_service.create(contest_uuid=contest_uuid, buy_in=5, wager=global_wager)
    assert contest.uuid is not None
    assert contest.contest_uuid == contest_uuid
    assert contest.buy_in == 5.0
    assert type(contest.buy_in) == float


def test_contest_create_w_wager_uuid():
    """
    GIVEN 1 contest instance in the database
    WHEN the create method is called with wager_uuid
    THEN it should return 1 contest and add 1 contest instance into the database
    """
    global global_wager
    contest_uuid = generate_uuid()
    contest = contest_service.create(contest_uuid=contest_uuid, buy_in=5.0, wager_uuid=global_wager.uuid)
    assert contest.uuid is not None
    assert contest.contest_uuid == contest_uuid
    assert contest.wager == global_wager
    assert contest.wager_uuid == global_wager.uuid


def test_contest_create_wo_contest_uuid(reset_db):
    """
    GIVEN 0 contest instance in the database
    WHEN the create method is called without contest_uuid
    THEN it should return 0 contest and add 0 contest instance into the database and ManualException with code 500
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    try:
        _ = contest_service.create(buy_in=5.0, wager_uuid=global_wager.uuid)
    except ManualException as ex:
        assert ex.code == 500
