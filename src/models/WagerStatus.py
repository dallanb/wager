from sqlalchemy_utils import generic_repr
from marshmallow_enum import EnumField
from ..common import WagerStatusEnum
from .. import db, ma
from .mixins import StatusMixin


class WagerStatus(db.Model, StatusMixin):
    name = db.Column(db.Enum(WagerStatusEnum), primary_key=True, unique=True, nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# class WagerStatusSchema(ma.SQLAlchemySchema):
#     name = EnumField(WagerStatusEnum)
#
#     class Meta:
#         model = WagerStatus
#         load_instance = True


WagerStatus.register()
