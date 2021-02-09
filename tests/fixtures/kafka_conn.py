import pytest

from src import app, Consumer, new_event_listener


@pytest.fixture(scope='session')
def kafka_conn():
    consumer = Consumer(topics=app.config['KAFKA_TOPICS'], event_listener=new_event_listener)
    consumer.start()
