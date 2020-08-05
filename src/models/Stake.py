from sqlalchemy_utils import CurrencyType, UUIDType, generic_repr
from .. import db
from ..models import Participant
from .mixins import BaseMixin


class Stake(db.Model, BaseMixin):
    currency = db.Column(CurrencyType)
    amount = db.Column(db.String)

    # FK
    participant_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('participant.uuid'), nullable=False)

    # Relationship
    participant = db.relationship("Participant")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Stake.register()
