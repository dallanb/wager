from src import services, ManualException
from tests.helpers import generate_uuid

global_payout = None
global_wager = None
payout_service = services.ContestService()


###########
# Find
###########
def test_payout_find(kafka_conn, reset_db, seed_payout):
    """
    GIVEN 1 payout instance in the database
    WHEN the find method is called with uuid
    THEN it should return 1 payout
    """

    global global_payout
    global global_wager

    payouts = payout_service.find()
    assert payouts.total == 1
    assert len(payouts.items) == 1
    global_payout = payouts.items[0]
    global_wager = payouts.items[0].wager


def test_payout_find_by_uuid(kafka_conn):
    """
    GIVEN 1 payout instance in the database
    WHEN the find method is called with uuid
    THEN it should return 1 payout
    """

    global global_payout
    payouts = payout_service.find(uuid=global_payout.uuid)
    assert payouts.total == 1
    assert len(payouts.items) == 1
    payout = payouts.items[0]
    assert payout.uuid == global_payout.uuid


def test_payout_find_by_wager_uuid(kafka_conn):
    """
    GIVEN 1 payout instance in the database
    WHEN the find method is called with wager_uuid
    THEN it should return 1 payout
    """

    global global_payout
    global global_wager

    payouts = payout_service.find(wager_uuid=global_wager.uuid)
    assert payouts.total == 1
    assert len(payouts.items) == 1
    payout = payouts.items[0]
    assert payout.wager.uuid == global_wager.uuid


def test_payout_find_w_pagination(kafka_conn, seed_payout):
    """
    GIVEN 2 payout instance in the database
    WHEN the find method is called with valid pagination
    THEN it should return 1 payout
    """
    payouts_0 = payout_service.find(page=1, per_page=1)
    assert payouts_0.total == 2
    assert len(payouts_0.items) == 1

    payouts_1 = payout_service.find(page=2, per_page=1)
    assert payouts_1.total == 2
    assert len(payouts_1.items) == 1
    assert payouts_1.items[0] != payouts_0.items[0]

    payouts = payout_service.find(page=1, per_page=2)
    assert payouts.total == 2
    assert len(payouts.items) == 2


def test_payout_find_by_payout_uuid_w_bad_pagination(kafka_conn, get_payout_uuid):
    """
    GIVEN 2 payout instance in the database
    WHEN the find method is called with out of range pagination
    THEN it should return 0 payout
    """
    payouts = payout_service.find(page=4, per_page=30)
    assert payouts.total == 2
    assert len(payouts.items) == 0


def test_payout_find_by_uuid_none_found(kafka_conn):
    """
    GIVEN 2 payout instance in the database
    WHEN the find method is called with random uuid
    THEN it should return 0 payout
    """
    payouts = payout_service.find(uuid=generate_uuid())
    assert payouts.total == 0
    assert len(payouts.items) == 0


def test_payout_find_by_non_existent_column(kafka_conn):
    """
    GIVEN 2 payout instance in the database
    WHEN the find method is called with random column
    THEN it should return 0 payout and ManualException with code 400
    """
    try:
        _ = payout_service.find(junk=generate_uuid())
    except ManualException as ex:
        assert ex.code == 400


def test_payout_find_by_non_existent_include(kafka_conn):
    """
    GIVEN 2 payout instance in the database
    WHEN the find method is called with include
    THEN it should return 0 payout and ManualException with code 400
    """

    try:
        _ = payout_service.find(include=['junk'])
    except ManualException as ex:
        assert ex.code == 400


def test_payout_find_by_non_existent_expand(kafka_conn):
    """
    GIVEN 2 payout instance in the database
    WHEN the find method is called with expand
    THEN it should return 0 payout and ManualException with code 400
    """

    try:
        _ = payout_service.find(expand=['junk'])
    except ManualException as ex:
        assert ex.code == 400


###########
# Create
###########
def test_payout_create(kafka_conn, reset_db, create_wager):
    """
    GIVEN 0 payout instance in the database
    WHEN the create method is called
    THEN it should return 1 payout and add 1 payout instance into the database
    """
    global global_payout
    global global_wager

    global_wager = create_wager(contest_uuid=generate_uuid(), buy_in=5.0)
    global_payout = payout_service.create(rank=1, proportion=0.75, wager=global_wager)
    payout = payout_service.create(rank=2, proportion=0.25, wager=global_wager)
    assert payout.uuid is not None
    assert payout.rank == 2
    assert payout.proportion == 0.25

    payouts = payout_service.find(uuid=global_payout.uuid)
    assert payouts.total == 1
    assert len(payouts.items) == 1


def test_payout_create_dup_payout_uuid(kafka_conn, get_payout_uuid):
    """
    GIVEN 1 payout instance in the database
    WHEN the create method is called with payout_uuid of payout already in the database
    THEN it should return 1 payout and add 1 payout instance into the database
    """
    wager = services.WagerService().create(status='active')
    payout_uuid = get_payout_uuid()
    payout = payout_service.create(payout_uuid=payout_uuid, buy_in=1.0, wager=wager)
    assert payout.uuid is not None
    assert payout.payout_uuid == payout_uuid
    assert payout.buy_in == 1.0

    payouts = payout_service.find(payout_uuid=payout_uuid)
    assert payouts.total == 2
    assert len(payouts.items) == 2


def test_payout_create_dup_wager(kafka_conn, get_payout_uuid):
    """
    GIVEN 2 payout instance in the database
    WHEN the create method is called with wager of payout already in the database
    THEN it should return 1 payout and add 1 payout instance into the database
    """
    global global_wager
    payout_uuid = generate_uuid()
    payout = payout_service.create(payout_uuid=payout_uuid, buy_in=4.0, wager=global_wager)
    assert payout.uuid is not None
    assert payout.payout_uuid == payout_uuid
    assert payout.buy_in == 4.0

    payouts = payout_service.find(uuid=global_payout.uuid)
    assert payouts.total == 1
    assert len(payouts.items) == 1

    payouts = payout_service.find(wager_uuid=global_wager.uuid)
    assert payouts.total == 2
    assert len(payouts.items) == 2


def test_payout_create_int_buy_in(kafka_conn, reset_db, get_payout_uuid):
    """
    GIVEN 0 payout instance in the database
    WHEN the create method is called with integer buy in
    THEN it should return 1 payout and add 1 payout instance into the database
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    payout_uuid = get_payout_uuid()
    payout = payout_service.create(payout_uuid=payout_uuid, buy_in=5, wager=global_wager)
    assert payout.uuid is not None
    assert payout.payout_uuid == payout_uuid
    assert payout.buy_in == 5.0
    assert type(payout.buy_in) == float


def test_payout_create_w_wager_uuid(kafka_conn):
    """
    GIVEN 1 payout instance in the database
    WHEN the create method is called with wager_uuid
    THEN it should return 1 payout and add 1 payout instance into the database
    """
    global global_wager
    payout_uuid = generate_uuid()
    payout = payout_service.create(payout_uuid=payout_uuid, buy_in=5.0, wager_uuid=global_wager.uuid)
    assert payout.uuid is not None
    assert payout.payout_uuid == payout_uuid
    assert payout.wager == global_wager
    assert payout.wager_uuid == global_wager.uuid


def test_payout_create_wo_payout_uuid(kafka_conn, reset_db):
    """
    GIVEN 0 payout instance in the database
    WHEN the create method is called without payout_uuid
    THEN it should return 0 payout and add 0 payout instance into the database and ManualException with code 500
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    try:
        _ = payout_service.create(buy_in=5.0, wager_uuid=global_wager.uuid)
    except ManualException as ex:
        assert ex.code == 500


def test_payout_create_wo_buy_in(kafka_conn, get_payout_uuid):
    """
    GIVEN 0 payout instance in the database
    WHEN the create method is called without buy in
    THEN it should return 1 payout and add 1 payout instance into the database
    """
    global global_wager
    payout_uuid = get_payout_uuid()

    payout = payout_service.create(payout_uuid=payout_uuid, wager_uuid=global_wager.uuid)
    assert payout.buy_in == 0.0
    assert type(payout.buy_in) == float


def test_payout_create_wo_wager(kafka_conn, reset_db, get_payout_uuid):
    """
    GIVEN 0 payout instance in the database
    WHEN the create method is called without wager
    THEN it should return 0 payout and add 0 payout instance into the database and ManualException with code 500
    """
    global global_wager
    payout_uuid = get_payout_uuid()

    try:
        _ = payout_service.create(payout_uuid=payout_uuid)
    except ManualException as ex:
        assert ex.code == 500


def test_payout_create_w_bad_field(kafka_conn, get_payout_uuid):
    """
    GIVEN 0 payout instance in the database
    WHEN the create method is called with a non existent field
    THEN it should return 0 payout and add 0 payout instance into the database and ManualException with code 500
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    payout_uuid = get_payout_uuid()

    try:
        _ = payout_service.create(payout_uuid=payout_uuid, buy_in=5.0, wager=global_wager, junk='junk')
    except ManualException as ex:
        assert ex.code == 500


def test_payout_create_w_bad_buy_in(kafka_conn, get_payout_uuid):
    """
    GIVEN 0 payout instance in the database
    WHEN the create method is called with a string buy_in
    THEN it should return 0 payout and add 0 payout instance into the database and ManualException with code 500
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    payout_uuid = get_payout_uuid()

    try:
        _ = payout_service.create(payout_uuid=payout_uuid, buy_in='five', wager=global_wager)
    except ManualException as ex:
        assert ex.code == 500


def test_payout_create_w_bad_payout_uuid(kafka_conn):
    """
    GIVEN 0 payout instance in the database
    WHEN the create method is called with an int payout_uuid
    THEN it should return 0 payout and add 0 payout instance into the database and ManualException with code 500
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')

    try:
        _ = payout_service.create(payout_uuid=1, buy_in=5.0, wager=global_wager)
    except ManualException as ex:
        assert ex.code == 500


def test_payout_create_w_non_existent_wager(kafka_conn, reset_db):
    """
    GIVEN 0 payout instance in the database
    WHEN the create method is called with a non existent wager
    THEN it should return 0 payout and add 0 payout instance into the database and ManualException with code 500
    """
    try:
        _ = payout_service.create(payout_uuid=generate_uuid(), buy_in=5.0, wager_uuid=generate_uuid())
    except ManualException as ex:
        assert ex.code == 500


###########
# Add
###########
def test_payout_add(kafka_conn, reset_db, get_payout_uuid):
    """
    GIVEN 0 payout instance in the database
    WHEN the add method is called
    THEN it should return 1 payout and add 0 payout instance into the database
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    payout_uuid = get_payout_uuid()
    payout = payout_service.add(payout_uuid=payout_uuid, buy_in=5.0, wager=global_wager)
    assert payout.uuid is not None
    assert payout.payout_uuid == payout_uuid
    assert payout.buy_in == 5.0

    payouts = payout_service.find(uuid=global_payout.uuid)
    assert payouts.total == 1
    assert len(payouts.items) == 1


def test_payout_add_dup_payout_uuid(kafka_conn, reset_db, get_payout_uuid):
    """
    GIVEN 1 payout instance in the database
    WHEN the add method is called with payout_uuid of payout already in the database
    THEN it should return 1 payout and add 0 payout instance into the database
    """
    wager = services.WagerService().create(status='active')
    payout_uuid = get_payout_uuid()
    payout = payout_service.create(payout_uuid=payout_uuid, buy_in=5.0, wager=wager)
    assert payout.uuid is not None

    payout_add = payout_service.add(payout_uuid=payout_uuid, buy_in=5.0, wager=wager)
    assert payout_add.uuid is not None

    assert payout.uuid != payout_add.uuid
    assert payout.payout_uuid == payout_add.payout_uuid

    payouts = payout_service.find(uuid=global_payout.uuid)
    assert payouts.total == 2
    assert len(payouts.items) == 2


def test_payout_add_int_buy_in(kafka_conn, reset_db, get_payout_uuid):
    """
    GIVEN 0 payout instance in the database
    WHEN the add method is called with integer buy in
    THEN it should return 1 payout and add 0 payout instance into the database
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    payout_uuid = get_payout_uuid()
    payout = payout_service.add(payout_uuid=payout_uuid, buy_in=5, wager=global_wager)
    assert payout.uuid is not None
    assert payout.payout_uuid == payout_uuid
    assert payout.buy_in == 5
    assert type(payout.buy_in) == int

    payouts = payout_service.find(uuid=global_payout.uuid)
    assert payouts.total == 1
    assert len(payouts.items) == 1


def test_payout_add_w_wager_uuid(kafka_conn, reset_db):
    """
    GIVEN 0 payout instance in the database
    WHEN the add method is called with wager_uuid
    THEN it should return 1 payout and add 0 payout instance into the database
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    payout_uuid = generate_uuid()
    payout = payout_service.add(payout_uuid=payout_uuid, buy_in=5.0, wager_uuid=global_wager.uuid)
    assert payout.uuid is not None
    assert payout.payout_uuid == payout_uuid
    assert payout.wager is None
    assert payout.wager_uuid == global_wager.uuid

    payouts = payout_service.find(uuid=global_payout.uuid)
    assert payouts.total == 1
    assert len(payouts.items) == 1


def test_payout_add_wo_payout_uuid(kafka_conn, reset_db):
    """
    GIVEN 0 payout instance in the database
    WHEN the add method is called without payout_uuid
    THEN it should return 1 payout and add 0 payout instance into the database
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    payout = payout_service.add(buy_in=5.0, wager_uuid=global_wager.uuid)
    assert payout.uuid is not None
    assert payout.payout_uuid is None
    payout_service.rollback()


def test_payout_add_wo_buy_in(kafka_conn, reset_db, get_payout_uuid):
    """
    GIVEN 0 payout instance in the database
    WHEN the add method is called without buy in
    THEN it should return 1 payout and add 0 payout instance into the database
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    payout_uuid = get_payout_uuid()

    payout = payout_service.add(payout_uuid=payout_uuid, wager_uuid=global_wager.uuid)
    assert payout.uuid is not None
    assert payout.buy_in is None

    payouts = payout_service.find(uuid=global_payout.uuid)
    assert payouts.total == 1
    assert len(payouts.items) == 1


def test_payout_add_wo_wager(kafka_conn, reset_db, get_payout_uuid):
    """
    GIVEN 0 payout instance in the database
    WHEN the add method is called without wager
    THEN it should return 1 payout and add 0 payout instance into the database
    """
    global global_wager
    payout_uuid = get_payout_uuid()

    payout = payout_service.add(payout_uuid=payout_uuid)
    assert payout.uuid is not None
    assert payout.wager is None
    payout_service.rollback()


def test_payout_add_w_bad_field(kafka_conn, get_payout_uuid):
    """
    GIVEN 0 payout instance in the database
    WHEN the add method is called with a non existent field
    THEN it should return 0 payout and add 0 payout instance into the database and ManualException with code 500
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    payout_uuid = get_payout_uuid()

    try:
        _ = payout_service.add(payout_uuid=payout_uuid, buy_in=5.0, wager=global_wager, junk='junk')
    except ManualException as ex:
        assert ex.code == 500


def test_payout_add_w_bad_buy_in(kafka_conn, get_payout_uuid):
    """
    GIVEN 0 payout instance in the database
    WHEN the add method is called with a string buy_in
    THEN it should return 1 payout and add 0 payout instance into the database
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    payout_uuid = get_payout_uuid()

    payout = payout_service.add(payout_uuid=payout_uuid, buy_in='five', wager=global_wager)
    assert payout.uuid is not None
    assert payout.buy_in == 'five'
    payout_service.rollback()


def test_payout_add_w_bad_payout_uuid(kafka_conn):
    """
    GIVEN 0 payout instance in the database
    WHEN the add method is called with an int payout_uuid
    THEN it should return 1 payout and add 0 payout instance into the database
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')

    payout = payout_service.add(payout_uuid=1, buy_in=5.0, wager=global_wager)
    assert payout.uuid is not None
    assert payout.payout_uuid == 1
    payout_service.rollback()


def test_payout_add_w_non_existent_wager(kafka_conn, reset_db):
    """
    GIVEN 0 payout instance in the database
    WHEN the add method is called with a non existent wager
    THEN it should return 0 payout and add 0 payout instance into the database
    """
    wager_uuid = generate_uuid()
    payout = payout_service.add(payout_uuid=generate_uuid(), buy_in=5.0, wager_uuid=wager_uuid)
    assert payout.uuid is not None
    assert payout.wager_uuid == wager_uuid
    payout_service.rollback()


###########
# Commit
###########
def test_payout_commit(kafka_conn, reset_db, get_payout_uuid):
    """
    GIVEN 0 payout instance in the database
    WHEN the commit method is called
    THEN it should return 0 payout and add 1 payout instance into the database
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    payout_uuid = get_payout_uuid()
    _ = payout_service.add(payout_uuid=payout_uuid, buy_in=5.0, wager=global_wager)
    _ = payout_service.commit()

    payouts = payout_service.find(uuid=global_payout.uuid)
    assert payouts.total == 1
    assert len(payouts.items) == 1


def test_payout_commit_dup_payout_uuid(kafka_conn, reset_db, get_payout_uuid):
    """
    GIVEN 1 payout instance in the database
    WHEN the commit method is called with payout_uuid of payout already in the database
    THEN it should return 0 payout and add 1 payout instance into the database
    """
    wager = services.WagerService().create(status='active')
    payout_uuid = get_payout_uuid()
    payout = payout_service.create(payout_uuid=payout_uuid, buy_in=5.0, wager=wager)
    assert payout.uuid is not None

    _ = payout_service.add(payout_uuid=payout_uuid, buy_in=5.0, wager=wager)
    _ = payout_service.commit()

    payouts = payout_service.find(uuid=global_payout.uuid)
    assert payouts.total == 2
    assert len(payouts.items) == 2


def test_payout_commit_int_buy_in(kafka_conn, reset_db, get_payout_uuid):
    """
    GIVEN 0 payout instance in the database
    WHEN the commit method is called with integer buy in
    THEN it should return 0 payout and add 1 payout instance into the database
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    payout_uuid = get_payout_uuid()
    _ = payout_service.add(payout_uuid=payout_uuid, buy_in=5, wager=global_wager)
    _ = payout_service.commit()

    payouts = payout_service.find(uuid=global_payout.uuid)
    assert payouts.total == 1
    assert len(payouts.items) == 1


def test_payout_commit_w_wager_uuid(kafka_conn, reset_db):
    """
    GIVEN 0 payout instance in the database
    WHEN the commit method is called with wager_uuid
    THEN it should return 0 payout and add 1 payout instance into the database
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    payout_uuid = generate_uuid()
    _ = payout_service.add(payout_uuid=payout_uuid, buy_in=5.0, wager_uuid=global_wager.uuid)
    _ = payout_service.commit()

    payouts = payout_service.find(uuid=global_payout.uuid)
    assert payouts.total == 1
    assert len(payouts.items) == 1


def test_payout_commit_wo_payout_uuid(kafka_conn, reset_db):
    """
    GIVEN 0 payout instance in the database
    WHEN the commit method is called without payout_uuid
    THEN it should return 0 payout and add 0 payout instance into the database and ManualException with code 500
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    _ = payout_service.add(buy_in=5.0, wager_uuid=global_wager.uuid)

    try:
        _ = payout_service.commit()
    except ManualException as ex:
        assert ex.code == 500


def test_payout_commit_wo_buy_in(kafka_conn, reset_db, get_payout_uuid):
    """
    GIVEN 0 payout instance in the database
    WHEN the commit method is called without buy in
    THEN it should return 0 payout and add 1 payout instance into the database
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    payout_uuid = get_payout_uuid()

    _ = payout_service.add(payout_uuid=payout_uuid, wager_uuid=global_wager.uuid)
    _ = payout_service.commit()

    payouts = payout_service.find(uuid=global_payout.uuid)
    assert payouts.total == 1
    assert len(payouts.items) == 1


def test_payout_commit_wo_wager(kafka_conn, reset_db, get_payout_uuid):
    """
    GIVEN 0 payout instance in the database
    WHEN the commit method is called without wager
    THEN it should return 0 payout and add 0 payout instance into the database and ManualException with code 500
    """
    global global_wager
    payout_uuid = get_payout_uuid()

    _ = payout_service.add(payout_uuid=payout_uuid)

    try:
        _ = payout_service.commit()
    except ManualException as ex:
        assert ex.code == 500


def test_payout_commit_w_bad_buy_in(kafka_conn, get_payout_uuid):
    """
    GIVEN 0 payout instance in the database
    WHEN the commit method is called with a string buy_in
    THEN it should return 0 payout and add 0 payout instance into the database and ManualException with code 500
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')
    payout_uuid = get_payout_uuid()

    _ = payout_service.add(payout_uuid=payout_uuid, buy_in='five', wager=global_wager)

    try:
        _ = payout_service.commit()
    except ManualException as ex:
        assert ex.code == 500


def test_payout_commit_w_bad_payout_uuid(kafka_conn):
    """
    GIVEN 0 payout instance in the database
    WHEN the commit method is called with an int payout_uuid
    THEN it should return 0 payout and add 0 payout instance into the database and ManualException with code 500
    """
    global global_wager
    global_wager = services.WagerService().create(status='active')

    _ = payout_service.add(payout_uuid=1, buy_in=5.0, wager=global_wager)

    try:
        _ = payout_service.commit()
    except ManualException as ex:
        assert ex.code == 500


def test_payout_commit_w_non_existent_wager(kafka_conn, reset_db):
    """
    GIVEN 0 payout instance in the database
    WHEN the commit method is called with a non existent wager
    THEN it should return 0 payout and add 0 payout instance into the database and ManualException with code 500
    """
    wager_uuid = generate_uuid()
    _ = payout_service.add(payout_uuid=generate_uuid(), buy_in=5.0, wager_uuid=wager_uuid)

    try:
        _ = payout_service.commit()
    except ManualException as ex:
        assert ex.code == 500
