from functools import wraps

from ...notifications import wager_created, payout_updated


class wager_notification:
    def __init__(self, operation):
        self.operation = operation

    def __call__(self, f):
        @wraps(f)
        def wrap(*args, **kwargs):
            new_instance = f(*args, **kwargs)

            if self.operation == 'create':
                self.create(new_instance=new_instance)
            elif self.operation == 'payout_update':
                self.payout_update(prev_instance=kwargs.get('instance'), new_instance=new_instance)
            return new_instance

        wrap.__doc__ = f.__doc__
        wrap.__name__ = f.__name__
        return wrap

    @staticmethod
    def create(new_instance):
        wager_created.from_data(wager=new_instance).notify()

    @staticmethod
    def payout_update(prev_instance, new_instance):
        if new_instance > 0:
            payout_updated.from_data(wager=prev_instance).notify()
