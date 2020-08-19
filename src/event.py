from .services import Contest


def new_event_listener(event):
    topic = event.topic
    key = event.key
    data = event.value

    if topic == 'contests':
        Contest().handle_event(key=key, data=data)
