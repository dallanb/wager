from src import services, ManualException
from tests.helpers import generate_uuid

global_party = None
global_participant = None
global_wager = None
party_service = services.PartyService()


###########
# Find
###########
def test_party_find(kafka_conn, reset_db, seed_party):
    """
    GIVEN 1 party instance in the database
    WHEN the find method is called
    THEN it should return 1 party
    """
    global global_party

    parties = party_service.find()

    assert parties.total == 1
    assert len(parties.items) == 1
    global_party = parties.items[0]


def test_party_find_by_uuid(kafka_conn):
    """
    GIVEN 1 party instance in the database
    WHEN the find method is called with uuid
    THEN it should return 1 party
    """
    global global_party
    parties = party_service.find(uuid=global_party.uuid)

    assert parties.total == 1
    assert len(parties.items) == 1
    party = parties.items[0]
    assert party.uuid == global_party.uuid


def test_party_find_include_participants(kafka_conn, get_member_uuid, create_participant):
    """
    GIVEN 1 party instance in the database
    WHEN the find method is called with uuid and with include argument to also return participants
    THEN it should return 1 party
    """
    global global_party
    global global_participant
    member_uuid = get_member_uuid()
    global_participant = create_participant(member_uuid=member_uuid, party_uuid=global_party.uuid)

    parties = party_service.find(uuid=global_party.uuid, include=['participants'])

    assert parties.total == 1
    assert len(parties.items) == 1
    party = parties.items[0]
    assert party.participants is not None
    assert len(party.participants) == 1
    assert party.participants[0].uuid == global_participant.uuid


def test_party_find_expand_wager(kafka_conn):
    """
    GIVEN 1 party instance in the database
    WHEN the find method is called with uuid and with expand argument to also return wager
    THEN it should return 1 party
    """
    global global_wager
    global global_party

    parties = party_service.find(uuid=global_party.uuid, expand=['wager'])

    assert parties.total == 1
    assert len(parties.items) == 1
    party = parties.items[0]
    assert party.wager is not None
    assert party.wager.uuid is not None
    global_wager = party.wager


def test_party_find_include_participants_expand_wager(kafka_conn):
    """
    GIVEN 1 party instance in the database
    WHEN the find method is called with uuid and with include argument to also return participants and with expand argument to also return wager
    THEN it should return 1 party
    """
    global global_party
    global global_participant
    global global_wager

    parties = party_service.find(uuid=global_party.uuid, include=['participants'], expand=['wager'])

    assert parties.total == 1
    assert len(parties.items) == 1
    party = parties.items[0]
    assert party.participants is not None
    assert len(party.participants) == 1
    assert party.participants[0].uuid == global_participant.uuid
    assert party.wager is not None
    assert party.wager.uuid == global_wager.uuid


def test_party_find_by_wager_uuid(kafka_conn, create_party):
    """
    GIVEN 1 party instance in the database
    WHEN the find method is called with wager_uuid
    THEN it should return as many party exist for that wager_uuid
    """
    global global_party
    global global_wager

    parties = party_service.find(wager_uuid=global_wager.uuid)

    assert parties.total == 1
    assert len(parties.items) == 1

    create_party(wager_uuid=global_wager.uuid)
    parties = party_service.find(wager_uuid=global_wager.uuid)

    assert parties.total == 2
    assert len(parties.items) == 2


def test_party_find_w_pagination(kafka_conn):
    """
    GIVEN 2 party instance in the database
    WHEN the find method is called with valid pagination
    THEN it should return the number of parties defined in the pagination arguments
    """
    parties_0 = party_service.find(page=1, per_page=1)
    assert parties_0.total == 2
    assert len(parties_0.items) == 1

    parties_1 = party_service.find(page=2, per_page=1)
    assert parties_1.total == 2
    assert len(parties_1.items) == 1
    assert parties_1.items[0] != parties_0.items[0]

    parties = party_service.find(page=1, per_page=2)
    assert parties.total == 2
    assert len(parties.items) == 2


def test_party_find_w_bad_pagination(kafka_conn):
    """
    GIVEN 2 party instance in the database
    WHEN the find method is called with invalid pagination
    THEN it should return the 0 party
    """
    parties = party_service.find(page=3, per_page=3)
    assert parties.total == 2
    assert len(parties.items) == 0


def test_party_find_by_non_existent_column(kafka_conn):
    """
    GIVEN 2 party instance in the database
    WHEN the find method is called with a random column
    THEN it should return the 0 party and ManualException with code 400
    """
    try:
        _ = party_service.find(junk=generate_uuid())
    except ManualException as ex:
        assert ex.code == 400


def test_party_find_by_non_existent_include(kafka_conn):
    """
    GIVEN 2 party instance in the database
    WHEN the find method is called with a random include
    THEN it should return the 0 party and ManualException with code 400
    """
    try:
        _ = party_service.find(include=['junk'])
    except ManualException as ex:
        assert ex.code == 400


def test_party_find_by_non_existent_expand(kafka_conn):
    """
    GIVEN 2 party instance in the database
    WHEN the find method is called with a random expand
    THEN it should return the 0 party and ManualException with code 400
    """
    try:
        _ = party_service.find(expand=['junk'])
    except ManualException as ex:
        assert ex.code == 400


###########
# Create
###########
def test_party_create(kafka_conn, reset_db, get_member_uuid, create_wager, create_party):
    """
    GIVEN 0 party instance in the database
    WHEN the create method is called
    THEN it should return 1 party and add 1 party instance into the database
    """
    global global_wager
    global global_party

    global_wager = create_wager(contest_uuid=generate_uuid(), buy_in=5.0)

    party = party_service.create(wager=global_wager)
    assert party.uuid is not None
    assert party.wager is not None


def test_party_create_dup_wager(kafka_conn, get_member_uuid):
    """
    GIVEN 1 party instance in the database
    WHEN the create method is called with duplicate wager
    THEN it should return 1 party and add 1 party instance into the database
    """
    global global_wager

    _ = party_service.create(wager=global_wager)

    parties = party_service.find()
    assert parties.total == 2
    assert len(parties.items) == 2


def test_party_create_w_wager_uuid(kafka_conn):
    """
    GIVEN 2 party instance in the database
    WHEN the create method is called with wager_uuid
    THEN it should return 1 party and add 1 party instance into the database
    """
    global global_wager

    party = party_service.create(wager_uuid=global_wager.uuid)
    assert party.uuid is not None


def test_party_create_wo_wager(kafka_conn):
    """
    GIVEN 3 party instance in the database
    WHEN the create method is called without wager
    THEN it should return 0 party and add 0 party instance into the database and ManualException with code 500
    """
    global global_wager

    try:
        _ = party_service.create()
    except ManualException as ex:
        assert ex.code == 500


def test_party_create_w_non_existent_wager_uuid(kafka_conn):
    """
    GIVEN 3 party instance in the database
    WHEN the create method is called with non existent wager uuid
    THEN it should return 0 party and add 0 party instance into the database and ManualException with code 500
    """
    global global_wager
    try:
        _ = party_service.create(wager_uuid=generate_uuid())
    except ManualException as ex:
        assert ex.code == 500


def test_party_create_w_bad_participants(kafka_conn):
    """
    GIVEN 3 party instance in the database
    WHEN the create method is called with participants array
    THEN it should return 0 party and add 0 party instance into the database and ManualException with code 500
    """
    global global_wager
    try:
        _ = party_service.create(wager=global_wager, member_uuid=generate_uuid(), participants=[global_wager])
    except ManualException as ex:
        assert ex.code == 500


def test_party_create_w_bad_field(kafka_conn):
    """
    GIVEN 3 party instance in the database
    WHEN the create method is called with a non existent field
    THEN it should return 0 party and add 0 party instance into the database and ManualException with code 500
    """
    global global_wager
    try:
        _ = party_service.create(wager=global_wager, junk='junk')
    except ManualException as ex:
        assert ex.code == 500


###########
# Add
###########
def test_party_add(kafka_conn, reset_db, create_wager):
    """
    GIVEN 0 party instance in the database
    WHEN the add method is called
    THEN it should return 1 party and add 0 party instance into the database
    """
    global global_wager
    global global_party
    global_wager = create_wager(contest_uuid=generate_uuid(), buy_in=5.0)
    party = party_service.add(wager=global_wager)
    assert party.uuid is not None
    assert party.wager == global_wager

    parties = party_service.find(uuid=party.uuid)
    assert parties.total == 1
    assert len(parties.items) == 1


def test_party_add_dup_wager(kafka_conn, get_member_uuid):
    """
    GIVEN 1 party instance in the database
    WHEN the add method is called with duplicate wager
    THEN it should return 1 party and add 0 party instance into the database
    """
    global global_wager

    party = party_service.add(wager=global_wager)
    assert party.wager == global_wager
    party_service.rollback()


def test_party_add_wo_wager(kafka_conn):
    """
    GIVEN 1 party instance in the database
    WHEN the add method is called without wager
    THEN it should return 1 party and add 0 party instance into the database
    """

    party = party_service.add()
    assert party.uuid is not None
    assert party.wager is None
    assert party.wager_uuid is None
    party_service.rollback()


def test_party_add_w_non_existent_wager_uuid(kafka_conn):
    """
    GIVEN 1 party instance in the database
    WHEN the add method is called with non existent wager uuid
    THEN it should return 1 party and add 0 party instance into the database
    """
    wager_uuid = generate_uuid()
    party = party_service.add(wager_uuid=wager_uuid)
    assert party.wager_uuid == wager_uuid
    party_service.rollback()


def test_party_add_w_bad_participants(kafka_conn):
    """
    GIVEN 1 party instance in the database
    WHEN the add method is called with participants array
    THEN it should return 0 party and add 0 party instance into the database and ManualException with code 500
    """
    global global_wager
    try:
        _ = party_service.add(wager=global_wager, participants=[global_party])
    except ManualException as ex:
        assert ex.code == 500


def test_party_add_w_bad_field(kafka_conn):
    """
    GIVEN 1 party instance in the database
    WHEN the add method is called with a non existent field
    THEN it should return 0 party and add 0 party instance into the database and ManualException with code 500
    """
    global global_wager
    try:
        _ = party_service.add(wager=global_wager, junk='junk')
    except ManualException as ex:
        assert ex.code == 500


###########
# Commit
###########
def test_party_commit(kafka_conn, reset_db, create_wager):
    """
    GIVEN 0 party instance in the database
    WHEN the commit method is called
    THEN it should return 0 party and add 1 party instance into the database
    """
    global global_wager

    global_wager = create_wager(contest_uuid=generate_uuid(), buy_in=5.0)
    _ = party_service.add(wager=global_wager)
    _ = party_service.commit()

    parties = party_service.find()
    assert parties.total == 1
    assert len(parties.items) == 1


def test_party_commit_dup_member_uuid_dup_wager(kafka_conn, get_member_uuid):
    """
    GIVEN 1 party instance in the database
    WHEN the commit method is called with duplicate wager
    THEN it should return 0 party and add 1 party instance into the database
    """
    global global_wager

    _ = party_service.add(wager=global_wager)
    _ = party_service.commit()

    parties = party_service.find()
    assert parties.total == 2
    assert len(parties.items) == 2


def test_party_commit_wo_wager(kafka_conn):
    """
    GIVEN 2 party instance in the database
    WHEN the commit method is called without wager
    THEN it should return 0 party and add 0 party instance into the database and ManualException with code 500
    """
    global global_wager

    _ = party_service.add()

    try:
        _ = party_service.commit()
    except ManualException as ex:
        assert ex.code == 500
