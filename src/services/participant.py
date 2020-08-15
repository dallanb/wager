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
        return Base.find(self, model=self.participant_model, **kwargs)

    def create(self, **kwargs):
        participant = self.init(model=self.participant_model, **kwargs)
        return self.save(instance=participant)

    def update(self, uuid, **kwargs):
        participants = self.find(uuid=uuid)
        if not participants.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        participant = self.assign_attr(instance=participants.items[0], attr=kwargs)
        return self.save(instance=participant)
