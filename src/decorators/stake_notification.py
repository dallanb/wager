from functools import wraps


class stake_notification:
    def __init__(self, operation):
        self.operation = operation
        self.topic = 'wagers'
        self._service = None

    def __call__(self, f):
        @wraps(f)
        def wrap(*args, **kwargs):
            self.service = args[0]
            new_instance = f(*args, **kwargs)

            if self.operation == 'create':
                self.create(new_instance=new_instance)

            return new_instance

        wrap.__doc__ = f.__doc__
        wrap.__name__ = f.__name__
        return wrap

    @property
    def service(self):
        return self._service

    @service.setter
    def service(self, service):
        self._service = service

    def create(self, new_instance):
        key = 'stake_created'
        value = {
            'uuid': str(new_instance.uuid),
            'member_uuid': str(new_instance.participant.member_uuid),
            'amount': new_instance.amount
        }
        self.service.notify(topic=self.topic, value=value, key=key, )
