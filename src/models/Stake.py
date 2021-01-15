from sqlalchemy_utils import CurrencyType, UUIDType
from .. import db
from .mixins import BaseMixin


class Stake(db.Model, BaseMixin):
    amount = db.Column(db.String)

    # FK
    participant_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('participant.uuid'), nullable=False)

    # Relationship
    participant = db.relationship("Participant", back_populates="stakes", lazy="noload")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Stake.register()
