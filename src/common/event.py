from .. import producer


class Event:
    @classmethod
    def _generate_endpoint(cls, topic, value):
        return {
            'endpoint': f"/{topic}/{str(value)}"
        }

    @classmethod
    def send(cls, topic, value, key):
        if producer.producer:
            producer.send(
                topic=topic,
                value=value,
                key=key
            )
