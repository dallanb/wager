import time

import pytest

from src import services
from tests.helpers import generate_uuid

contest_service = services.ContestService()
wager_service = services.WagerService()


def test_wager_notification_operation_create(reset_db, kafka_conn_last_msg):
    """
    GIVEN 0 contest instance in the database
    WHEN the wager service create method is called
    THEN it should allow the wager_notification decorator to send an event
    """
    contest = contest_service.create(contest_uuid=pytest.contest_uuid)
    wager = wager_service.create(status='active', contest=contest)
    msg = kafka_conn_last_msg('wagers')
    assert msg.key is not None
    assert msg.key == 'wager_created'
    assert msg.value is not None
    assert msg.value['uuid'] == str(wager.uuid)


def test_wager_notification_operation_payout_update(reset_db, kafka_conn_last_msg):
    """
    GIVEN 0 contest instance in the database
    WHEN the wager service create method is called
    THEN it should allow the wager_notification decorator to send an event
    """
    buy_in = 5.0
    payout = [0.70, 0.20, 0.10]
    contest_uuid = pytest.contest_uuid
    contest = contest_service.create(contest_uuid=contest_uuid, buy_in=buy_in)
    wager = wager_service.create(status='active', contest=contest)
    wager_service.validate_and_create_payout(instance=wager, payout_list=payout)
    for index in range(2):
        party = services.PartyService().add(wager=wager)
        participant = services.ParticipantService().add(member_uuid=generate_uuid(),
                                                        status='active', party=party)
        _ = services.StakeService().create(amount=buy_in, participant=participant)
    wager_service.check_payout(instance=wager)
    time.sleep(0.2)
    msg = kafka_conn_last_msg('wagers')
    assert msg.key is not None
    assert msg.key == 'payout_updated'
    assert msg.value is not None
    assert msg.value['uuid'] == str(wager.uuid)
