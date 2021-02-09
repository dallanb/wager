from src import services, ManualException
from tests.helpers import generate_uuid

global_contest = None
global_wager = None
contest_service = services.ContestService()


###########
# Find
###########
def test_contest_find_by_contest_uuid(kafka_conn, reset_db, get_contest_uuid, create_wager):
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


def test_contest_find_by_uuid(kafka_conn):
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


def test_contest_find_include_wager(kafka_conn):
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


def test_contest_find_by_wager_uuid(kafka_conn):
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


def test_contest_find_by_contest_uuid_multiple(kafka_conn, get_contest_uuid, create_wager):
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


def test_contest_find_by_contest_uuid_multiple_match_single(kafka_conn, reset_db, get_contest_uuid, create_wager):
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


def test_contest_find_by_contest_uuid_w_pagination(kafka_conn, get_contest_uuid):
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


def test_contest_find_by_contest_uuid_w_bad_pagination(kafka_conn, get_contest_uuid):
    """
    GIVEN 2 contest instance in the database
    WHEN the find method is called with contest_uuid and out of range pagination
    THEN it should return 0 contest
    """
    contest_uuid = get_contest_uuid()

    contests = contest_service.find(contest_uuid=contest_uuid, page=4, per_page=30)
    assert contests.total == 1
    assert len(contests.items) == 0


def test_contest_find_by_contest_uuid_none_found(kafka_conn, reset_db, get_contest_uuid):
    """
    GIVEN 0 contest instance in the database
    WHEN the find method is called with contest_uuid
    THEN it should return 0 contest
    """
    contest_uuid = get_contest_uuid()

    contests = contest_service.find(contest_uuid=contest_uuid)
    assert contests.total == 0
    assert len(contests.items) == 0


def test_contest_find_by_non_existent_column(kafka_conn, reset_db, get_contest_uuid, create_wager):
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


def test_contest_find_by_non_existent_include(kafka_conn, get_contest_uuid, create_wager):
    """
    GIVEN 0 contest instance in the database
    WHEN the find method is called with include
    THEN it should return 0 contest and ManualException with code 400
    """

    try:
        _ = contest_service.find(include=['junk'])
    except ManualException as ex:
        assert ex.code == 400


def test_contest_find_by_non_existent_expand(kafka_conn, get_contest_uuid, create_wager):
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
def test_contest_create(kafka_conn, reset_db, get_contest_uuid):
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


def test_contest_create_dup_contest_uuid(kafka_conn, get_contest_uuid):
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


def test_contest_create_dup_wager(kafka_conn, get_contest_uuid):
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


def test_contest_create_int_buy_in(kafka_conn, reset_db, get_contest_uuid):
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


def test_contest_create_w_wager_uuid(kafka_conn):
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


def test_contest_create_wo_contest_uuid(kafka_conn, reset_db):
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


def test_contest_create_wo_buy_in(kafka_conn, get_contest_uuid):
    """
    GIVEN 0 contest instance in the database
    WHEN the create method is called without buy in
    THEN it should return 1 contest and add 1 contest instance into the database
    """
    global global_wager
    contest_uuid = get_contest_uuid()

    contest = contest_service.create(contest_uuid=contest_uuid, wager_uuid=global_wager.uuid)
    assert contest.buy_in == 0.0
    assert type(contest.buy_in) == float


def test_contest_create_wo_wager(kafka_conn, reset_db, get_contest_uuid):
    """
    GIVEN 0 contest instance in the database
    WHEN the create method is called without wager
    THEN it should return 0 contest and add 0 contest instance into the database and ManualException with code 500
    """
    global global_wager
    contest_uuid = get_contest_uuid()

    try:
        _ = contest_service.create(contest_uuid=contest_uuid)
    except ManualException as ex:
        assert ex.code == 500


def test_contest_create_w_bad_field(kafka_conn, get_contest_uuid):
    """
    GIVEN 0 contest instance in the database
    WHEN the create method is called with a non existent field
    THEN it should return 0 contest and add 0 contest instance into the database and ManualException with code 500
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    contest_uuid = get_contest_uuid()

    try:
        _ = contest_service.create(contest_uuid=contest_uuid, buy_in=5.0, wager=global_wager, junk='junk')
    except ManualException as ex:
        assert ex.code == 500


def test_contest_create_w_bad_buy_in(kafka_conn, get_contest_uuid):
    """
    GIVEN 0 contest instance in the database
    WHEN the create method is called with a string buy_in
    THEN it should return 0 contest and add 0 contest instance into the database and ManualException with code 500
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    contest_uuid = get_contest_uuid()

    try:
        _ = contest_service.create(contest_uuid=contest_uuid, buy_in='five', wager=global_wager)
    except ManualException as ex:
        assert ex.code == 500


def test_contest_create_w_bad_contest_uuid(kafka_conn):
    """
    GIVEN 0 contest instance in the database
    WHEN the create method is called with an int contest_uuid
    THEN it should return 0 contest and add 0 contest instance into the database and ManualException with code 500
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')

    try:
        _ = contest_service.create(contest_uuid=1, buy_in=5.0, wager=global_wager)
    except ManualException as ex:
        assert ex.code == 500


def test_contest_create_w_non_existent_wager(kafka_conn, reset_db):
    """
    GIVEN 0 contest instance in the database
    WHEN the create method is called with a non existent wager
    THEN it should return 0 contest and add 0 contest instance into the database and ManualException with code 500
    """
    try:
        _ = contest_service.create(contest_uuid=generate_uuid(), buy_in=5.0, wager_uuid=generate_uuid())
    except ManualException as ex:
        assert ex.code == 500


###########
# Add
###########
def test_contest_add(kafka_conn, reset_db, get_contest_uuid):
    """
    GIVEN 0 contest instance in the database
    WHEN the add method is called
    THEN it should return 1 contest and add 0 contest instance into the database
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    contest_uuid = get_contest_uuid()
    contest = contest_service.add(contest_uuid=contest_uuid, buy_in=5.0, wager=global_wager)
    assert contest.uuid is not None
    assert contest.contest_uuid == contest_uuid
    assert contest.buy_in == 5.0

    contests = contest_service.find(contest_uuid=contest_uuid)
    assert contests.total == 1
    assert len(contests.items) == 1


def test_contest_add_dup_contest_uuid(kafka_conn, reset_db, get_contest_uuid):
    """
    GIVEN 1 contest instance in the database
    WHEN the add method is called with contest_uuid of contest already in the database
    THEN it should return 1 contest and add 0 contest instance into the database
    """
    wager = services.WagerService().create(status='active')
    contest_uuid = get_contest_uuid()
    contest = contest_service.create(contest_uuid=contest_uuid, buy_in=5.0, wager=wager)
    assert contest.uuid is not None

    contest_add = contest_service.add(contest_uuid=contest_uuid, buy_in=5.0, wager=wager)
    assert contest_add.uuid is not None

    assert contest.uuid != contest_add.uuid
    assert contest.contest_uuid == contest_add.contest_uuid

    contests = contest_service.find(contest_uuid=contest_uuid)
    assert contests.total == 2
    assert len(contests.items) == 2


def test_contest_add_int_buy_in(kafka_conn, reset_db, get_contest_uuid):
    """
    GIVEN 0 contest instance in the database
    WHEN the add method is called with integer buy in
    THEN it should return 1 contest and add 0 contest instance into the database
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    contest_uuid = get_contest_uuid()
    contest = contest_service.add(contest_uuid=contest_uuid, buy_in=5, wager=global_wager)
    assert contest.uuid is not None
    assert contest.contest_uuid == contest_uuid
    assert contest.buy_in == 5
    assert type(contest.buy_in) == int

    contests = contest_service.find(contest_uuid=contest_uuid)
    assert contests.total == 1
    assert len(contests.items) == 1


def test_contest_add_w_wager_uuid(kafka_conn, reset_db):
    """
    GIVEN 0 contest instance in the database
    WHEN the add method is called with wager_uuid
    THEN it should return 1 contest and add 0 contest instance into the database
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    contest_uuid = generate_uuid()
    contest = contest_service.add(contest_uuid=contest_uuid, buy_in=5.0, wager_uuid=global_wager.uuid)
    assert contest.uuid is not None
    assert contest.contest_uuid == contest_uuid
    assert contest.wager is None
    assert contest.wager_uuid == global_wager.uuid

    contests = contest_service.find(contest_uuid=contest_uuid)
    assert contests.total == 1
    assert len(contests.items) == 1


def test_contest_add_wo_contest_uuid(kafka_conn, reset_db):
    """
    GIVEN 0 contest instance in the database
    WHEN the add method is called without contest_uuid
    THEN it should return 1 contest and add 0 contest instance into the database
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    contest = contest_service.add(buy_in=5.0, wager_uuid=global_wager.uuid)
    assert contest.uuid is not None
    assert contest.contest_uuid is None
    contest_service.db.rollback()


def test_contest_add_wo_buy_in(kafka_conn, reset_db, get_contest_uuid):
    """
    GIVEN 0 contest instance in the database
    WHEN the add method is called without buy in
    THEN it should return 1 contest and add 0 contest instance into the database
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    contest_uuid = get_contest_uuid()

    contest = contest_service.add(contest_uuid=contest_uuid, wager_uuid=global_wager.uuid)
    assert contest.uuid is not None
    assert contest.buy_in is None

    contests = contest_service.find(contest_uuid=contest_uuid)
    assert contests.total == 1
    assert len(contests.items) == 1


def test_contest_add_wo_wager(kafka_conn, reset_db, get_contest_uuid):
    """
    GIVEN 0 contest instance in the database
    WHEN the add method is called without wager
    THEN it should return 1 contest and add 0 contest instance into the database
    """
    global global_wager
    contest_uuid = get_contest_uuid()

    contest = contest_service.add(contest_uuid=contest_uuid)
    assert contest.uuid is not None
    assert contest.wager is None
    contest_service.db.rollback()


def test_contest_add_w_bad_field(kafka_conn, get_contest_uuid):
    """
    GIVEN 0 contest instance in the database
    WHEN the add method is called with a non existent field
    THEN it should return 0 contest and add 0 contest instance into the database and ManualException with code 500
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    contest_uuid = get_contest_uuid()

    try:
        _ = contest_service.add(contest_uuid=contest_uuid, buy_in=5.0, wager=global_wager, junk='junk')
    except ManualException as ex:
        assert ex.code == 500


def test_contest_add_w_bad_buy_in(kafka_conn, get_contest_uuid):
    """
    GIVEN 0 contest instance in the database
    WHEN the add method is called with a string buy_in
    THEN it should return 1 contest and add 0 contest instance into the database
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    contest_uuid = get_contest_uuid()

    contest = contest_service.add(contest_uuid=contest_uuid, buy_in='five', wager=global_wager)
    assert contest.uuid is not None
    assert contest.buy_in == 'five'
    contest_service.db.rollback()


def test_contest_add_w_bad_contest_uuid(kafka_conn):
    """
    GIVEN 0 contest instance in the database
    WHEN the add method is called with an int contest_uuid
    THEN it should return 1 contest and add 0 contest instance into the database
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')

    contest = contest_service.add(contest_uuid=1, buy_in=5.0, wager=global_wager)
    assert contest.uuid is not None
    assert contest.contest_uuid == 1
    contest_service.db.rollback()


def test_contest_add_w_non_existent_wager(kafka_conn, reset_db):
    """
    GIVEN 0 contest instance in the database
    WHEN the add method is called with a non existent wager
    THEN it should return 0 contest and add 0 contest instance into the database
    """
    wager_uuid = generate_uuid()
    contest = contest_service.add(contest_uuid=generate_uuid(), buy_in=5.0, wager_uuid=wager_uuid)
    assert contest.uuid is not None
    assert contest.wager_uuid == wager_uuid
    contest_service.db.rollback()


###########
# Commit
###########
def test_contest_commit(kafka_conn, reset_db, get_contest_uuid):
    """
    GIVEN 0 contest instance in the database
    WHEN the commit method is called
    THEN it should return 0 contest and add 1 contest instance into the database
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    contest_uuid = get_contest_uuid()
    _ = contest_service.add(contest_uuid=contest_uuid, buy_in=5.0, wager=global_wager)
    _ = contest_service.commit()

    contests = contest_service.find(contest_uuid=contest_uuid)
    assert contests.total == 1
    assert len(contests.items) == 1


def test_contest_commit_dup_contest_uuid(kafka_conn, reset_db, get_contest_uuid):
    """
    GIVEN 1 contest instance in the database
    WHEN the commit method is called with contest_uuid of contest already in the database
    THEN it should return 0 contest and add 1 contest instance into the database
    """
    wager = services.WagerService().create(status='active')
    contest_uuid = get_contest_uuid()
    contest = contest_service.create(contest_uuid=contest_uuid, buy_in=5.0, wager=wager)
    assert contest.uuid is not None

    _ = contest_service.add(contest_uuid=contest_uuid, buy_in=5.0, wager=wager)
    _ = contest_service.commit()

    contests = contest_service.find(contest_uuid=contest_uuid)
    assert contests.total == 2
    assert len(contests.items) == 2


def test_contest_commit_int_buy_in(kafka_conn, reset_db, get_contest_uuid):
    """
    GIVEN 0 contest instance in the database
    WHEN the commit method is called with integer buy in
    THEN it should return 0 contest and add 1 contest instance into the database
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    contest_uuid = get_contest_uuid()
    _ = contest_service.add(contest_uuid=contest_uuid, buy_in=5, wager=global_wager)
    _ = contest_service.commit()

    contests = contest_service.find(contest_uuid=contest_uuid)
    assert contests.total == 1
    assert len(contests.items) == 1


def test_contest_commit_w_wager_uuid(kafka_conn, reset_db):
    """
    GIVEN 0 contest instance in the database
    WHEN the commit method is called with wager_uuid
    THEN it should return 0 contest and add 1 contest instance into the database
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    contest_uuid = generate_uuid()
    _ = contest_service.add(contest_uuid=contest_uuid, buy_in=5.0, wager_uuid=global_wager.uuid)
    _ = contest_service.commit()

    contests = contest_service.find(contest_uuid=contest_uuid)
    assert contests.total == 1
    assert len(contests.items) == 1


def test_contest_commit_wo_contest_uuid(kafka_conn, reset_db):
    """
    GIVEN 0 contest instance in the database
    WHEN the commit method is called without contest_uuid
    THEN it should return 0 contest and add 0 contest instance into the database and ManualException with code 500
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    _ = contest_service.add(buy_in=5.0, wager_uuid=global_wager.uuid)

    try:
        _ = contest_service.commit()
    except ManualException as ex:
        assert ex.code == 500


def test_contest_commit_wo_buy_in(kafka_conn, reset_db, get_contest_uuid):
    """
    GIVEN 0 contest instance in the database
    WHEN the commit method is called without buy in
    THEN it should return 0 contest and add 1 contest instance into the database
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    contest_uuid = get_contest_uuid()

    _ = contest_service.add(contest_uuid=contest_uuid, wager_uuid=global_wager.uuid)
    _ = contest_service.commit()

    contests = contest_service.find(contest_uuid=contest_uuid)
    assert contests.total == 1
    assert len(contests.items) == 1


def test_contest_commit_wo_wager(kafka_conn, reset_db, get_contest_uuid):
    """
    GIVEN 0 contest instance in the database
    WHEN the commit method is called without wager
    THEN it should return 0 contest and add 0 contest instance into the database and ManualException with code 500
    """
    global global_wager
    contest_uuid = get_contest_uuid()

    _ = contest_service.add(contest_uuid=contest_uuid)

    try:
        _ = contest_service.commit()
    except ManualException as ex:
        assert ex.code == 500


def test_contest_commit_w_bad_buy_in(kafka_conn, get_contest_uuid):
    """
    GIVEN 0 contest instance in the database
    WHEN the commit method is called with a string buy_in
    THEN it should return 0 contest and add 0 contest instance into the database and ManualException with code 500
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    contest_uuid = get_contest_uuid()

    _ = contest_service.add(contest_uuid=contest_uuid, buy_in='five', wager=global_wager)

    try:
        _ = contest_service.commit()
    except ManualException as ex:
        assert ex.code == 500


def test_contest_commit_w_bad_contest_uuid(kafka_conn):
    """
    GIVEN 0 contest instance in the database
    WHEN the commit method is called with an int contest_uuid
    THEN it should return 0 contest and add 0 contest instance into the database and ManualException with code 500
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')

    _ = contest_service.add(contest_uuid=1, buy_in=5.0, wager=global_wager)

    try:
        _ = contest_service.commit()
    except ManualException as ex:
        assert ex.code == 500


def test_contest_commit_w_non_existent_wager(kafka_conn, reset_db):
    """
    GIVEN 0 contest instance in the database
    WHEN the commit method is called with a non existent wager
    THEN it should return 0 contest and add 0 contest instance into the database and ManualException with code 500
    """
    wager_uuid = generate_uuid()
    _ = contest_service.add(contest_uuid=generate_uuid(), buy_in=5.0, wager_uuid=wager_uuid)

    try:
        _ = contest_service.commit()
    except ManualException as ex:
        assert ex.code == 500
