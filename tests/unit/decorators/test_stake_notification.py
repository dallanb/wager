import pytest

from src import services

stake_service = services.StakeService()


def test_stake_notification_operation_create(reset_db, kafka_conn_last_msg, seed_wager, seed_party, seed_participant):
    """
    GIVEN 0 contest instance in the database
    WHEN the stake service create method is called
    THEN it should allow the stake_notification decorator to send an event
    """
    stake = stake_service.create(participant=pytest.participant, amount=pytest.buy_in)
    msg = kafka_conn_last_msg('wagers')
    assert msg.key is not None
    assert msg.key == 'stake_created'
    assert msg.value is not None
    assert msg.value['uuid'] == str(stake.uuid)
    assert msg.value['member_uuid'] == str(stake.participant.member_uuid)
    assert msg.value['amount'] == stake.amount
