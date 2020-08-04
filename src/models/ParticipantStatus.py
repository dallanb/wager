from sqlalchemy_utils import generic_repr
from marshmallow_enum import EnumField
from ..common import ParticipantStatusEnum
from .. import db, ma
from .mixins import StatusMixin


@generic_repr('name')
class ParticipantStatus(db.Model, StatusMixin):
    name = db.Column(db.Enum(ParticipantStatusEnum), primary_key=True, unique=True, nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ParticipantStatusSchema(ma.SQLAlchemySchema):
    name = EnumField(ParticipantStatusEnum)

    class Meta:
        model = ParticipantStatus
        load_instance = True


ParticipantStatus.register()
