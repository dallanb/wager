from sqlalchemy_utils import UUIDType, generic_repr
from .. import db
from ..models import Party, ParticipantStatus
from ..common import ParticipantStatusEnum
from .mixins import BaseMixin


class Participant(db.Model, BaseMixin):
    user_uuid = db.Column(UUIDType(binary=False), nullable=False)

    # FK
    party_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('party.uuid'), nullable=False)
    status = db.Column(db.Enum(ParticipantStatusEnum), db.ForeignKey('participant_status.name'), nullable=False)

    # Relationship
    party = db.relationship("Party")
    participant_status = db.relationship("ParticipantStatus")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Participant.register()
