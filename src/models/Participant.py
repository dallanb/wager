from sqlalchemy.orm import validates
from sqlalchemy_utils import UUIDType

from .mixins import BaseMixin
from .. import db
from ..common import ParticipantStatusEnum


class Participant(db.Model, BaseMixin):
    # Constraints
    __table_args__ = (db.UniqueConstraint('member_uuid', 'party_uuid', name='member_party'),)

    member_uuid = db.Column(UUIDType(binary=False), nullable=False)

    # FK
    party_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('party.uuid'), nullable=False)
    status = db.Column(db.Enum(ParticipantStatusEnum), db.ForeignKey('participant_status.name'), nullable=False)

    # Relationship
    party = db.relationship("Party", back_populates="participants")
    participant_status = db.relationship("ParticipantStatus")
    stakes = db.relationship("Stake", back_populates="participant")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @validates('member_uuid')
    def validates_member_uuid(self, key, value):
        if self.member_uuid:  # Field already exists
            raise ValueError('member_uuid cannot be modified.')

        return value

    @validates('party_uuid')
    def validates_party_uuid(self, key, value):
        if self.party_uuid:  # Field already exists
            raise ValueError('party_uuid cannot be modified.')

        return value


Participant.register()
