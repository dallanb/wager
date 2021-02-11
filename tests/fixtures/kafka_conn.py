import pytest
import json

from kafka import KafkaConsumer, TopicPartition, OffsetAndMetadata

from src import app, Consumer, new_event_listener


@pytest.fixture(scope='session')
def kafka_conn():
    consumer = Consumer(topics=app.config['KAFKA_TOPICS'], event_listener=new_event_listener)
    consumer.start()


@pytest.fixture
def kafka_conn_custom():
    def _method(topic):
        consumer = KafkaConsumer(bootstrap_servers='wager_kafka:9092', group_id='testing',
                                 key_deserializer=bytes.decode,
                                 value_deserializer=lambda v: json.loads(v.decode('utf-8')), auto_offset_reset='latest',
                                 enable_auto_commit=False)

        partition = TopicPartition(topic, 0)
        consumer.assign([partition])
        last_pos = consumer.end_offsets([partition])
        pos = last_pos[partition]
        offset = OffsetAndMetadata(pos - 1, b'')
        consumer.commit(offsets={partition: offset})
        msg = next(consumer)
        consumer.close()
        return msg

    return _method
