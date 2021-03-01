import logging
from functools import wraps

from src.notifications import participant_active, participant_inactive


class participant_notification:
    def __init__(self, operation):
        self.operation = operation

    def __call__(self, f):
        @wraps(f)
        def wrap(*args, **kwargs):
            prev_instance = {**kwargs.get('instance').__dict__} if kwargs.get('instance') else None
            new_instance = f(*args, **kwargs)

            if self.operation == 'update':
                self.update(prev_instance=prev_instance, new_instance=new_instance)
            return new_instance

        wrap.__doc__ = f.__doc__
        wrap.__name__ = f.__name__
        return wrap

    @staticmethod
    def update(prev_instance, new_instance):
        if prev_instance and prev_instance.get('status') and prev_instance['status'].name != new_instance.status.name:
            if new_instance.status.name == 'active':
                participant_active.from_data(participant=new_instance).notify()
            elif new_instance.status.name == 'inactive':
                participant_inactive.from_data(participant=new_instance).notify()
