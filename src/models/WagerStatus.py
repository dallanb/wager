from sqlalchemy_utils import generic_repr
from marshmallow_enum import EnumField
from ..common import WagerStatusEnum
from .. import db, ma
from .mixins import BaseMixin


@generic_repr('id', 'uuid')
class WagerStatus(db.Model, BaseMixin):
    name = db.Column(db.Enum(WagerStatusEnum), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class WagerStatusSchema(ma.SQLAlchemySchema):
    name = EnumField(WagerStatusEnum)

    class Meta:
        model = WagerStatus
        load_instance = True

    uuid = ma.auto_field()


WagerStatus.register()
