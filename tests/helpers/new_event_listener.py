import logging

from src.events import Contest


def new_event_listener(event):
    topic = event.topic
    key = event.key
    data = event.value
    if topic == 'contests_test':
        try:
            Contest().handle_event(key=key, data=data)
        except Exception as ex:
            logging.info(ex)
            logging.info('contest error')
