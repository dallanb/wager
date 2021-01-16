from sqlalchemy_utils import UUIDType, generic_repr
from .. import db
from ..common import ParticipantStatusEnum
from .mixins import BaseMixin


class Participant(db.Model, BaseMixin):
    member_uuid = db.Column(UUIDType(binary=False), nullable=False)

    # FK
    party_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('party.uuid'), nullable=False)
    status = db.Column(db.Enum(ParticipantStatusEnum), db.ForeignKey('participant_status.name'), nullable=False)

    # Relationship
    party = db.relationship("Party", back_populates="participants", lazy="noload")
    participant_status = db.relationship("ParticipantStatus")
    stakes = db.relationship("Stake", back_populates="participant", lazy="noload")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Participant.register()
