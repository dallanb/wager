import logging
from .base import Base
from ..models import Participant as ParticipantModel
from http import HTTPStatus


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

    def create(self, **kwargs):
        participant = self._init(model=self.participant_model, **kwargs)
        return self._save(instance=participant)

    def update(self, uuid, **kwargs):
        participants = self.find(uuid=uuid)
        if not participants.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        participant = self.assign_attr(instance=participants.items[0], attr=kwargs)
        return self._save(instance=participant)
