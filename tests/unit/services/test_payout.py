import pytest

from src import services, ManualException
from tests.helpers import generate_uuid

payout_service = services.PayoutService()


###########
# Find
###########
def test_payout_find(kafka_conn, reset_db, seed_wager, seed_payouts):
    """
    GIVEN 2 payout instance in the database
    WHEN the find method is called
    THEN it should return 2 payout
    """

    payouts = payout_service.find()
    assert payouts.total == 2
    assert len(payouts.items) == 2


def test_payout_find_by_uuid(kafka_conn):
    """
    GIVEN 2 payout instance in the database
    WHEN the find method is called with uuid
    THEN it should return 1 payout
    """

    payouts = payout_service.find(uuid=pytest.payouts[0].uuid)
    assert payouts.total == 1
    assert len(payouts.items) == 1
    payout = payouts.items[0]
    assert payout.uuid == pytest.payouts[0].uuid


def test_payout_find_by_wager_uuid(kafka_conn):
    """
    GIVEN 2 payout instance in the database
    WHEN the find method is called with wager_uuid
    THEN it should return 1 payout
    """

    payouts = payout_service.find(wager_uuid=pytest.wager.uuid)
    assert payouts.total == 2
    assert len(payouts.items) == 2
    payout = payouts.items[0]
    assert payout.wager.uuid == pytest.wager.uuid


def test_payout_find_w_pagination(kafka_conn):
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


def test_payout_find_by_payout_uuid_w_bad_pagination(kafka_conn):
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
