from ..libs import Producer


class Event:
    @classmethod
    def send(cls, topic, value, key):
        producer = Producer(topic=topic, value=value, key=key)
        producer.start()
