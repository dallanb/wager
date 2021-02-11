from src import services

wager_service = services.WagerService()


def test_wager_notification_operation_create(reset_db, kafka_conn_last_mg):
    """
    GIVEN 0 contest instance in the database
    WHEN the wager service create method is called
    THEN it should allow the wager_notification decorator to send an event
    """
    wager = wager_service.create(status='active')
    msg = kafka_conn_last_mg('wagers')
    assert msg.key is not None
    assert msg.key == 'wager_created'
    assert msg.value is not None
    assert msg.value['uuid'] == str(wager.uuid)
