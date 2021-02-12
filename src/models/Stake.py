from sqlalchemy.orm import validates
from sqlalchemy_utils import UUIDType

from .mixins import BaseMixin
from .. import db


class Stake(db.Model, BaseMixin):
    amount = db.Column(db.Float, nullable=False, default=0.0)

    # FK
    participant_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('participant.uuid'), nullable=False, unique=True)

    # Relationship
    participant = db.relationship("Participant", back_populates="stake")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @validates('amount')
    def validates_amount(self, key, value):
        if self.amount:  # Field already exists
            raise ValueError('amount cannot be modified.')

        return value


Stake.register()
