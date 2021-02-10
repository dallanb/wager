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


def test_participant_find_include_stakes_expand_party(kafka_conn):
    """
    GIVEN 1 participant instance in the database
    WHEN the find method is called with uuid and with include argument to also return stakes and with expand argument to also return party
    THEN it should return 1 participant
    """
    global global_participant
    global global_stake
    global global_party

    participants = participant_service.find(uuid=global_participant.uuid, include=['stakes'], expand=['party'])

    assert participants.total == 1
    assert len(participants.items) == 1
    participant = participants.items[0]
    assert participant.stakes is not None
    assert len(participant.stakes) == 1
    assert participant.stakes[0].uuid == global_stake.uuid
    assert participant.party is not None
    assert participant.party.uuid == global_party.uuid


def test_participant_find_by_party_uuid(kafka_conn):
    """
    GIVEN 1 participant instance in the database
    WHEN the find method is called with party_uuid
    THEN it should return 1 participant
    """
    global global_participant
    global global_party

    participants = participant_service.find(party_uuid=global_party.uuid)

    assert participants.total == 1
    assert len(participants.items) == 1


def test_participant_find_multiple(kafka_conn, get_member_uuid, create_wager, create_party,
                                   create_participant):
    """
    GIVEN 2 participant instance in the database
    WHEN the find method is called
    THEN it should return 2 participant
    """
    global global_participant
    member_uuid = get_member_uuid()
    wager = create_wager(contest_uuid=generate_uuid(), buy_in=5.0)
    party = create_party(wager_uuid=wager.uuid)
    _ = create_participant(party_uuid=party.uuid, member_uuid=member_uuid)

    participants = participant_service.find()

    assert participants.total == 2
    assert len(participants.items) == 2


def test_participant_find_by_member_uuid_multiple(kafka_conn, get_member_uuid):
    """
    GIVEN 2 participant instance in the database
    WHEN the find method is called with member_uuid
    THEN it should return 2 participant
    """
    global global_participant
    member_uuid = get_member_uuid()

    participants = participant_service.find(member_uuid=member_uuid)

    assert participants.total == 2
    assert len(participants.items) == 2


def test_participant_find_by_party_uuid_multiple_match_single(kafka_conn):
    """
    GIVEN 2 participant instance in the database
    WHEN the find method is called with party_uuid
    THEN it should return 1 participant
    """
    global global_participant
    global global_party

    participants = participant_service.find(party_uuid=global_party.uuid)

    assert participants.total == 1
    assert len(participants.items) == 1
    assert participants.items[0].party.uuid == global_party.uuid


def test_participant_find_w_pagination(kafka_conn):
    """
    GIVEN 2 participant instance in the database
    WHEN the find method is called with valid pagination
    THEN it should return the number of participants defined in the pagination arguments
    """
    participants_0 = participant_service.find(page=1, per_page=1)
    assert participants_0.total == 2
    assert len(participants_0.items) == 1

    participants_1 = participant_service.find(page=2, per_page=1)
    assert participants_1.total == 2
    assert len(participants_1.items) == 1
    assert participants_1.items[0] != participants_0.items[0]

    participants = participant_service.find(page=1, per_page=2)
    assert participants.total == 2
    assert len(participants.items) == 2


def test_participant_find_w_bad_pagination(kafka_conn):
    """
    GIVEN 2 participant instance in the database
    WHEN the find method is called with invalid pagination
    THEN it should return the 0 participant
    """
    participants = participant_service.find(page=3, per_page=3)
    assert participants.total == 2
    assert len(participants.items) == 0


def test_participant_find_by_member_uuid_none_found(kafka_conn):
    """
    GIVEN 2 participant instance in the database
    WHEN the find method is called with a random member_uuid
    THEN it should return the 0 participant
    """
    participants = participant_service.find(member_uuid=generate_uuid())
    assert participants.total == 0
    assert len(participants.items) == 0


def test_participant_find_by_non_existent_column(kafka_conn):
    """
    GIVEN 2 participant instance in the database
    WHEN the find method is called with a random column
    THEN it should return the 0 participant and ManualException with code 400
    """
    try:
        _ = participant_service.find(junk=generate_uuid())
    except ManualException as ex:
        assert ex.code == 400


def test_participant_find_by_non_existent_include(kafka_conn):
    """
    GIVEN 2 participant instance in the database
    WHEN the find method is called with a random include
    THEN it should return the 0 participant and ManualException with code 400
    """
    try:
        _ = participant_service.find(include=['junk'])
    except ManualException as ex:
        assert ex.code == 400


def test_participant_find_by_non_existent_expand(kafka_conn):
    """
    GIVEN 2 participant instance in the database
    WHEN the find method is called with a random expand
    THEN it should return the 0 participant and ManualException with code 400
    """
    try:
        _ = participant_service.find(expand=['junk'])
    except ManualException as ex:
        assert ex.code == 400


###########
# Create
###########
def test_participant_create(kafka_conn, reset_db, get_member_uuid, create_wager, create_party):
    """
    GIVEN 0 participant instance in the database
    WHEN the create method is called
    THEN it should return 1 participant and add 1 participant instance into the database
    """
    global global_wager
    global global_party

    member_uuid = get_member_uuid()
    global_wager = create_wager(contest_uuid=generate_uuid(), buy_in=5.0)
    global_party = create_party(wager_uuid=global_wager.uuid)

    participant = participant_service.create(party=global_party, member_uuid=member_uuid, status='active')
    assert participant.uuid is not None
    assert participant.member_uuid == member_uuid
    assert participant.party is not None


def test_participant_create_dup_member_uuid_dup_party(kafka_conn, get_member_uuid):
    """
    GIVEN 1 participant instance in the database
    WHEN the create method is called with duplicate member_uuid and duplicate party
    THEN it should return 0 participant and add 0 participant instance into the database and ManualException with code 500
    """
    global global_wager
    global global_party

    member_uuid = get_member_uuid()

    try:
        _ = participant_service.create(party=global_party, member_uuid=member_uuid, status='active')
    except ManualException as ex:
        assert ex.code == 500


def test_participant_create_dup_member_uuid(kafka_conn, get_member_uuid, create_wager, create_party):
    """
    GIVEN 1 participant instance in the database
    WHEN the create method is called with duplicate member_uuid
    THEN it should return 1 participant and add 1 participant instance into the database
    """
    global global_wager
    global global_party

    member_uuid = get_member_uuid()
    wager = create_wager(contest_uuid=generate_uuid(), buy_in=5.0)
    party = create_party(wager_uuid=wager.uuid)
    participant = participant_service.create(party=party, member_uuid=member_uuid, status='active')
    assert participant.member_uuid == member_uuid

    participants = participant_service.find(member_uuid=member_uuid)
    assert participants.total == 2
    assert len(participants.items) == 2


def test_participant_create_dup_party(kafka_conn):
    """
    GIVEN 2 participant instance in the database
    WHEN the create method is called with duplicate party
    THEN it should return 1 participant and add 1 participant instance into the database
    """
    global global_wager
    global global_party

    participant = participant_service.create(party=global_party, member_uuid=generate_uuid(), status='active')
    assert participant.uuid is not None
    assert participant.party == global_party


def test_participant_create_w_party_uuid(kafka_conn):
    """
    GIVEN 3 participant instance in the database
    WHEN the create method is called with party_uuid
    THEN it should return 1 participant and add 1 participant instance into the database
    """
    global global_wager
    global global_party

    participant = participant_service.create(party_uuid=global_party.uuid, member_uuid=generate_uuid(), status='active')
    assert participant.uuid is not None
    assert participant.party == global_party


def test_participant_create_wo_party(kafka_conn):
    """
    GIVEN 3 participant instance in the database
    WHEN the create method is called without party
    THEN it should return 0 participant and add 0 participant instance into the database and ManualException with code 500
    """
    global global_wager

    try:
        _ = participant_service.create(member_uuid=generate_uuid(), status='active')
    except ManualException as ex:
        assert ex.code == 500


def test_participant_create_wo_member_uuid(kafka_conn):
    """
    GIVEN 3 participant instance in the database
    WHEN the create method is called without member_uuid
    THEN it should return 0 participant and add 0 participant instance into the database and ManualException with code 500
    """
    global global_wager
    global global_party
    try:
        _ = participant_service.create(party=global_party, status='active')
    except ManualException as ex:
        assert ex.code == 500


def test_participant_create_wo_status(kafka_conn):
    """
    GIVEN 3 participant instance in the database
    WHEN the create method is called without status
    THEN it should return 0 participant and add 0 participant instance into the database and ManualException with code 500
    """
    global global_wager
    try:
        _ = participant_service.create(party=global_party, member_uuid=generate_uuid())
    except ManualException as ex:
        assert ex.code == 500


def test_participant_create_w_non_existent_party_uuid(kafka_conn):
    """
    GIVEN 3 participant instance in the database
    WHEN the create method is called with non existent party uuid
    THEN it should return 0 participant and add 0 participant instance into the database and ManualException with code 500
    """
    global global_wager
    try:
        _ = participant_service.create(party_uuid=generate_uuid(), member_uuid=generate_uuid(), status='active')
    except ManualException as ex:
        assert ex.code == 500


def test_participant_create_w_non_existent_status(kafka_conn):
    """
    GIVEN 3 participant instance in the database
    WHEN the create method is called with non existent status
    THEN it should return 0 participant and add 0 participant instance into the database and ManualException with code 500
    """
    global global_wager
    global global_party
    try:
        _ = participant_service.create(party=global_party, member_uuid=generate_uuid(), status='radioactive')
    except ManualException as ex:
        assert ex.code == 500


def test_participant_create_w_bad_stakes(kafka_conn):
    """
    GIVEN 3 participant instance in the database
    WHEN the create method is called with stakes array
    THEN it should return 0 participant and add 0 participant instance into the database and ManualException with code 500
    """
    global global_wager
    global global_party
    try:
        _ = participant_service.create(party=global_party, member_uuid=generate_uuid(), status='active',
                                       stakes=[global_party])
    except ManualException as ex:
        assert ex.code == 500


def test_participant_create_w_bad_field(kafka_conn):
    """
    GIVEN 3 participant instance in the database
    WHEN the create method is called with a non existent field
    THEN it should return 0 participant and add 0 participant instance into the database and ManualException with code 500
    """
    global global_wager
    global global_party
    try:
        _ = participant_service.create(party=global_party, member_uuid=generate_uuid(), status='active', junk='junk')
    except ManualException as ex:
        assert ex.code == 500


###########
# Add
###########
def test_participant_add(kafka_conn, reset_db, get_member_uuid, create_wager, create_party):
    """
    GIVEN 0 participant instance in the database
    WHEN the add method is called
    THEN it should return 1 participant and add 0 participant instance into the database
    """
    global global_wager
    global global_party
    member_uuid = get_member_uuid()
    global_wager = create_wager(contest_uuid=generate_uuid(), buy_in=5.0)
    global_party = create_party(wager_uuid=global_wager.uuid)
    participant = participant_service.add(party=global_party, member_uuid=member_uuid, status='active')
    assert participant.uuid is not None
    assert participant.member_uuid == member_uuid
    assert participant.party == global_party

    participants = participant_service.find(uuid=participant.uuid)
    assert participants.total == 1
    assert len(participants.items) == 1


def test_participant_add_dup_member_uuid_dup_party(kafka_conn, get_member_uuid):
    """
    GIVEN 1 participant instance in the database
    WHEN the add method is called with duplicate member_uuid and duplicate party
    THEN it should return 1 participant and add 0 participant instance into the database
    """
    global global_wager
    global global_party

    member_uuid = get_member_uuid()

    participants = participant_service.find(member_uuid=member_uuid)
    assert participants.total == 1
    assert len(participants.items) == 1

    participant = participant_service.add(party=global_party, member_uuid=member_uuid, status='active')
    assert participant.party == participants.items[0].party
    assert participant.member_uuid == participants.items[0].member_uuid

    participant_service.rollback()


def test_participant_add_w_party_uuid(kafka_conn):
    """
    GIVEN 1 participant instance in the database
    WHEN the add method is called with party_uuid
    THEN it should return 1 participant and add 0 participant instance into the database
    """
    global global_wager
    global global_party

    participant = participant_service.add(party_uuid=global_party.uuid, member_uuid=generate_uuid(), status='active')
    assert participant.uuid is not None
    assert participant.party is None
    assert participant.party_uuid == global_party.uuid
    participant_service.rollback()


def test_participant_add_wo_party(kafka_conn):
    """
    GIVEN 1 participant instance in the database
    WHEN the add method is called without party
    THEN it should return 1 participant and add 0 participant instance into the database
    """
    global global_wager

    participant = participant_service.add(member_uuid=generate_uuid(), status='active')
    assert participant.uuid is not None
    assert participant.party is None
    assert participant.party_uuid is None
    participant_service.rollback()


def test_participant_add_w_non_existent_party_uuid(kafka_conn):
    """
    GIVEN 1 participant instance in the database
    WHEN the add method is called with non existent party uuid
    THEN it should return 1 participant and add 0 participant instance into the database
    """
    global global_wager

    party_uuid = generate_uuid()
    participant = participant_service.add(party_uuid=party_uuid, member_uuid=generate_uuid(), status='active')
    assert participant.party_uuid == party_uuid
    participant_service.rollback()


def test_participant_add_w_bad_stakes(kafka_conn):
    """
    GIVEN 1 participant instance in the database
    WHEN the add method is called with stakes array
    THEN it should return 0 participant and add 0 participant instance into the database and ManualException with code 500
    """
    global global_wager
    global global_party
    try:
        _ = participant_service.add(party=global_party, member_uuid=generate_uuid(), status='active',
                                    stakes=[global_party])
    except ManualException as ex:
        assert ex.code == 500


def test_participant_add_w_bad_field(kafka_conn):
    """
    GIVEN 1 participant instance in the database
    WHEN the add method is called with a non existent field
    THEN it should return 0 participant and add 0 participant instance into the database and ManualException with code 500
    """
    global global_wager
    global global_party
    try:
        _ = participant_service.add(party=global_party, member_uuid=generate_uuid(), status='active', junk='junk')
    except ManualException as ex:
        assert ex.code == 500


###########
# Commit
###########
def test_participant_commit(kafka_conn, reset_db, get_member_uuid, create_wager, create_party):
    """
    GIVEN 0 participant instance in the database
    WHEN the commit method is called
    THEN it should return 0 participant and add 1 participant instance into the database
    """
    global global_wager
    global global_party
    member_uuid = get_member_uuid()
    global_wager = create_wager(contest_uuid=generate_uuid(), buy_in=5.0)
    global_party = create_party(wager_uuid=global_wager.uuid)
    _ = participant_service.add(party=global_party, member_uuid=member_uuid, status='active')
    _ = participant_service.commit()

    participants = participant_service.find()
    assert participants.total == 1
    assert len(participants.items) == 1


def test_participant_commit_dup_member_uuid_dup_party(kafka_conn, get_member_uuid):
    """
    GIVEN 1 participant instance in the database
    WHEN the commit method is called with duplicate member_uuid and duplicate party
    THEN it should return 0 participant and add 0 participant instance into the database and ManualException with code 500
    """
    global global_wager
    global global_party

    member_uuid = get_member_uuid()

    _ = participant_service.find(member_uuid=member_uuid)

    _ = participant_service.add(party=global_party, member_uuid=member_uuid, status='active')

    try:
        _ = participant_service.commit()
    except ManualException as ex:
        assert ex.code == 500


def test_participant_commit_w_party_uuid(kafka_conn):
    """
    GIVEN 1 participant instance in the database
    WHEN the commit method is called with party_uuid
    THEN it should return 0 participant and add 1 participant instance into the database
    """
    global global_wager
    global global_party

    member_uuid = generate_uuid()
    _ = participant_service.add(party_uuid=global_party.uuid, member_uuid=member_uuid, status='active')

    _ = participant_service.commit()

    participants = participant_service.find(member_uuid=member_uuid)
    assert participants.total == 1
    assert len(participants.items) == 1


def test_participant_commit_wo_party(kafka_conn):
    """
    GIVEN 2 participant instance in the database
    WHEN the commit method is called without party
    THEN it should return 0 participant and add 0 participant instance into the database and ManualException with code 500
    """
    global global_wager

    _ = participant_service.add(member_uuid=generate_uuid(), status='active')

    try:
        _ = participant_service.commit()
    except ManualException as ex:
        assert ex.code == 500


###########
# Update
###########
def test_participant_update(kafka_conn, reset_db, seed_participant):
    """
    GIVEN 1 participant instance in the database
    WHEN the update method is called
    THEN it should return 1 participant and update 1 participant instance in the database
    """
    global global_participant
    participants = participant_service.find()
    global_participant = participants.items[0]
    assert global_participant.status.name == 'pending'

    participant_service.update(uuid=global_participant.uuid, status='active')
    assert global_participant.status.name == 'active'


def test_participant_update_member_uuid(kafka_conn):
    """
    GIVEN 1 participant instance in the database
    WHEN the update method is called with member_uuid
    THEN it should return 0 participant and update 0 participant instance in the database and ManualException with code 400
    """
    global global_participant

    try:
        _ = participant_service.update(uuid=global_participant.uuid, member_uuid=generate_uuid())
    except ManualException as ex:
        assert ex.code == 400


def test_participant_update_party_uuid(kafka_conn):
    """
    GIVEN 1 participant instance in the database
    WHEN the update method is called with party_uuid
    THEN it should return 0 participant and update 0 participant instance in the database and ManualException with code 400
    """
    global global_participant

    try:
        _ = participant_service.update(uuid=global_participant.uuid, party_uuid=generate_uuid())
    except ManualException as ex:
        assert ex.code == 400


def test_participant_update_party(kafka_conn):
    """
    GIVEN 1 participant instance in the database
    WHEN the update method is called with party
    THEN it should return 0 participant and update 0 participant instance in the database and ManualException with code 400
    """
    global global_participant

    try:
        _ = participant_service.update(uuid=global_participant.uuid, party=generate_uuid())
    except ManualException as ex:
        assert ex.code == 400


def test_participant_update_w_bad_uuid(kafka_conn):
    """
    GIVEN 1 participant instance in the database
    WHEN the update method is called with random uuid
    THEN it should return 0 participant and update 0 participant instance in the database and ManualException with code 404
    """
    global global_participant

    try:
        _ = participant_service.update(uuid=generate_uuid(), status='inactive')
    except ManualException as ex:
        assert ex.code == 404


def test_participant_update_w_bad_field(kafka_conn):
    """
    GIVEN 1 participant instance in the database
    WHEN the update method is called with random uuid
    THEN it should return 1 participant and update 0 participant instance in the database
    """
    global global_participant

    try:
        _ = participant_service.update(uuid=global_participant.uuid, junk='junk')
    except ManualException as ex:
        assert ex.code == 400
