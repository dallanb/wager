import time

import pytest

from src import services

participant_service = services.ParticipantService()


def test_participant_notification_participant_active(reset_db, kafka_conn_last_msg, seed_wager, seed_party,
                                                     seed_participant, seed_stake):
    """
    GIVEN 1 wager instance, 1 contest instance, 1 party instance, 1 participant instance in the database
    WHEN the participant service update method is called with status active
    THEN it should allow the participant_notification decorator to send an event
    """
    participant = participant_service.update(uuid=pytest.participant.uuid, status='active')
    time.sleep(0.2)
    msg = kafka_conn_last_msg('wagers')
    assert msg.key is not None
    assert msg.key == 'participant_active'
    assert msg.value is not None
    assert msg.value['uuid'] == str(participant.uuid)
    assert msg.value['member_uuid'] == str(participant.member_uuid)
    assert msg.value['stake'] == pytest.buy_in


def test_participant_notification_participant_inactive(reset_db, kafka_conn_last_msg, seed_wager, seed_party,
                                                       seed_participant, seed_stake):
    """
    GIVEN 1 wager instance, 1 contest instance, 1 party instance, 1 participant instance in the database
    WHEN the participant service update method is called with status inactive
    THEN it should allow the participant_notification decorator to send an event
    """
    participant = participant_service.update(uuid=pytest.participant.uuid, status='inactive')
    time.sleep(0.2)
    msg = kafka_conn_last_msg('wagers')
    assert msg.key is not None
    assert msg.key == 'participant_inactive'
    assert msg.value is not None
    assert msg.value['uuid'] == str(participant.uuid)
    assert msg.value['member_uuid'] == str(participant.member_uuid)
    assert msg.value['stake'] == pytest.buy_in
