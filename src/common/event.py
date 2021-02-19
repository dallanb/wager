from ..libs import Producer


class Event:
    @staticmethod
    def send(topic, value, key):
        producer = Producer(topic=topic, value=value, key=key)
        producer.start()
