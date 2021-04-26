import logging
from http import HTTPStatus

from .base import Base
from ..decorators.notifications import participant_notification
from ..models import Participant as ParticipantModel


class Participant(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.participant_model = ParticipantModel

    def find(self, **kwargs):
        return self._find(model=self.participant_model, **kwargs)

    def add(self, **kwargs):
        participant = self._init(model=self.participant_model, **kwargs)
        return self._add(instance=participant)

    def commit(self):
        return self._commit()

    def create(self, **kwargs):
        participant = self._init(model=self.participant_model, **kwargs)
        return self._save(instance=participant)

    def update(self, uuid, **kwargs):
        participants = self.find(uuid=uuid)
        if not participants.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=participants.items[0], **kwargs)

    @participant_notification(operation='update')
    def apply(self, instance, **kwargs):
        participant = self._assign_attr(instance=instance, attr=kwargs)
        return self._save(instance=participant)

    def rollback(self):
        return self._rollback()
