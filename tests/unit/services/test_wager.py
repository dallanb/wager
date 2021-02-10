from src import services, ManualException
from tests.helpers import generate_uuid

global_party = None
global_wager = None
wager_service = services.WagerService()


###########
# Find
###########
def test_wager_find(kafka_conn, reset_db, seed_wager):
    """
    GIVEN 1 wager instance in the database
    WHEN the find method is called
    THEN it should return 1 wager
    """
    global global_wager

    wagers = wager_service.find()

    assert wagers.total == 1
    assert len(wagers.items) == 1
    global_wager = wagers.items[0]


def test_wager_find_by_uuid(kafka_conn):
    """
    GIVEN 1 wager instance in the database
    WHEN the find method is called with uuid
    THEN it should return 1 wager
    """
    global global_wager

    wagers = wager_service.find(uuid=global_wager.uuid)

    assert wagers.total == 1
    assert len(wagers.items) == 1
    assert wagers.items[0].uuid == global_wager.uuid


def test_wager_find_include_parties(kafka_conn, create_party):
    """
    GIVEN 1 wager instance in the database
    WHEN the find method is called with include argument to return parties
    THEN it should return 1 wager
    """
    global global_wager

    party = create_party(wager_uuid=global_wager.uuid)
    wagers = wager_service.find(include=['parties'])

    wager = wagers.items[0]
    assert wager.parties is not None
    assert len(wager.parties) == 1
    assert wager.parties[0].uuid == party.uuid


def test_wager_find_include_payouts(kafka_conn):
    """
    GIVEN 1 wager instance in the database
    WHEN the find method is called with include argument to return payouts
    THEN it should return 1 wager
    """
    global global_wager

    # creating 2 payouts here
    payouts = wager_service.validate_and_create_payout(instance=global_wager, payout_list=[0.75, 0.25])
    wagers = wager_service.find(include=['payouts'])

    wager = wagers.items[0]
    assert wager.payouts is not None
    assert len(wager.payouts) == 2


def test_wager_find_include_parties_and_payouts(kafka_conn):
    """
    GIVEN 1 wager instance in the database
    WHEN the find method is called with include argument to return parties and payouts
    THEN it should return 1 wager
    """
    global global_wager

    wagers = wager_service.find(include=['parties', 'payouts'])

    wager = wagers.items[0]
    assert wager.parties is not None
    assert len(wager.parties) == 1
    assert wager.payouts is not None
    assert len(wager.payouts) == 2


def test_wager_find_w_pagination(kafka_conn, seed_wager):
    """
    GIVEN 2 wager instance in the database
    WHEN the find method is called with valid pagination
    THEN it should return the number of wagers defined in the pagination argument
    """
    wagers_0 = wager_service.find(page=1, per_page=1)
    assert wagers_0.total == 2
    assert len(wagers_0.items) == 1

    wagers_1 = wager_service.find(page=2, per_page=1)
    assert wagers_1.total == 2
    assert len(wagers_1.items) == 1
    assert wagers_1.items[0] != wagers_0.items[0]

    wagers = wager_service.find(page=1, per_page=2)
    assert wagers.total == 2
    assert len(wagers.items) == 2


def test_wager_find_w_bad_pagination(kafka_conn):
    """
    GIVEN 2 wager instance in the database
    WHEN the find method is called with invalid pagination
    THEN it should return the 0 wager
    """
    wagers = wager_service.find(page=3, per_page=3)
    assert wagers.total == 2
    assert len(wagers.items) == 0


def test_wager_find_by_non_existent_column(kafka_conn):
    """
    GIVEN 2 wager instance in the database
    WHEN the find method is called with a random column
    THEN it should return the 0 wager and ManualException with code 400
    """
    try:
        _ = wager_service.find(junk=generate_uuid())
    except ManualException as ex:
        assert ex.code == 400


def test_wager_find_by_non_existent_include(kafka_conn):
    """
    GIVEN 2 wager instance in the database
    WHEN the find method is called with a random include
    THEN it should return the 0 wager and ManualException with code 400
    """
    try:
        _ = wager_service.find(include=['junk'])
    except ManualException as ex:
        assert ex.code == 400


def test_wager_find_by_non_existent_expand(kafka_conn):
    """
    GIVEN 2 wager instance in the database
    WHEN the find method is called with a random expand
    THEN it should return the 0 wager and ManualException with code 400
    """
    try:
        _ = wager_service.find(expand=['junk'])
    except ManualException as ex:
        assert ex.code == 400


###########
# Create
###########
def test_wager_create(kafka_conn, reset_db):
    """
    GIVEN 0 wager instance in the database
    WHEN the create method is called
    THEN it should return 1 wager and add 1 wager instance into the database
    """
    global global_wager

    global_wager = wager_service.create(status='active')

    assert global_wager.uuid is not None
    assert global_wager.status.name == 'active'


def test_wager_create_wo_status(kafka_conn, reset_db):
    """
    GIVEN 1 wager instance in the database
    WHEN the create method is called without status
    THEN it should return 1 wager and add 1 wager instance into the database
    """
    wager = wager_service.create()

    assert wager.uuid is not None
    assert wager.status.name == 'pending'


def test_wager_create_w_non_existent_status(kafka_conn):
    """
    GIVEN 1 wager instance in the database
    WHEN the create method is called with a non existent status
    THEN it should return 0 wager and add 0 wager instance into the database and ManualException with code 500
    """
    try:
        _ = wager_service.create(status='junk')
    except ManualException as ex:
        assert ex.code == 500


def test_wager_create_w_bad_parties(kafka_conn):
    """
    GIVEN 1 wager instance in the database
    WHEN the create method is called with parties array
    THEN it should return 0 wager and add 0 wager instance into the database and ManualException with code 500
    """
    try:
        _ = wager_service.create(status='active', parties=[generate_uuid()])
    except ManualException as ex:
        assert ex.code == 500


def test_wager_create_w_bad_payouts(kafka_conn):
    """
    GIVEN 1 wager instance in the database
    WHEN the create method is called with payouts array
    THEN it should return 0 wager and add 0 wager instance into the database and ManualException with code 500
    """
    try:
        _ = wager_service.create(status='active', payouts=[generate_uuid()])
    except ManualException as ex:
        assert ex.code == 500


def test_wager_create_w_bad_field(kafka_conn):
    """
    GIVEN 1 wager instance in the database
    WHEN the create method is called with a non existent field
    THEN it should return 0 wager and add 0 wager instance into the database and ManualException with code 500
    """
    global global_wager
    try:
        _ = wager_service.create(status='active', junk='junk')
    except ManualException as ex:
        assert ex.code == 500


###########
# Misc
###########
def test_party_validate_and_create_payout(kafka_conn, reset_db, seed_wager):
    """
    GIVEN 1 wager instance in the database and 0 payout instance in the database
    WHEN the validate_and_create_payout method is called with valid parameters
    THEN it should return an array of payout instances
    """
    global global_wager
    wagers = wager_service.find()
    global_wager = wagers.items[0]

    payout_list = [0.75, 0.25]
    payouts = wager_service.validate_and_create_payout(instance=global_wager, payout_list=payout_list)

    assert len(payouts) == 2
    for payout in payouts:
        assert payout.proportion in payout_list

    wagers = wager_service.find(include=['payouts'])
    assert wagers.total == 1
    assert len(wagers.items[0].payouts) == 2


def test_party_validate_and_create_payout_w_existing_payout(kafka_conn):
    """
    GIVEN 1 wager instance in the database and 2 payout instance in the database
    WHEN the validate_and_create_payout method is called with valid parameters
    THEN it should return ManualException with code 400 and msg 'payout can only be added once for a wager'
    """
    global global_wager
    payout_list = [1.0]

    try:
        _ = wager_service.validate_and_create_payout(instance=global_wager, payout_list=payout_list)
    except ManualException as ex:
        assert ex.code == 400
        assert ex.msg == 'payout can only be added once for a wager'


def test_party_validate_and_create_payout_invalid_params(kafka_conn, reset_db, seed_wager):
    """
    GIVEN 1 wager instance in the database and 0 payout instance in the database
    WHEN the validate_and_create_payout method is called with invalid parameters
    THEN it should return ManualException with code 400
    """
    wagers = wager_service.find()
    wager = wagers.items[0]

    payout_list = [0.75, 0.30]

    try:
        _ = wager_service.validate_and_create_payout(instance=wager, payout_list=payout_list)
    except ManualException as ex:
        assert ex.code == 400
