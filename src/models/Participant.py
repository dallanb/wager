from sqlalchemy_utils import UUIDType, generic_repr
from marshmallow_enum import EnumField
from .. import db, ma
from ..models import Party, ParticipantStatus
from ..common import ParticipantStatusEnum
from .mixins import BaseMixin


@generic_repr('id', 'uuid')
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


class ParticipantSchema(ma.SQLAlchemySchema):
    status = EnumField(ParticipantStatusEnum)

    class Meta:
        model = Participant
        load_instance = True

    uuid = ma.auto_field()
    user_uuid = ma.auto_field()


Participant.register()
