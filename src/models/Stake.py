from sqlalchemy_utils import CurrencyType, UUIDType, generic_repr
from .. import db, ma
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

#
# class StakeSchema(ma.SQLAlchemySchema):
#     class Meta:
#         model = Stake
#         load_instance = True
#
#     uuid = ma.auto_field()
#     currency = ma.auto_field()
#     amount = ma.auto_field()
#     participant = ma.auto_field()


Stake.register()
