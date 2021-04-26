import logging
import traceback

from .events import *


def new_event_listener(event):
    topic = event.topic
    key = event.key
    data = event.value
    if topic == 'contests':
        try:
            Contest().handle_event(key=key, data=data)
        except Exception as ex:
            logging.error(traceback.format_exc())
            logging.error('contest error')
