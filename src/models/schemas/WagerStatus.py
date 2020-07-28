from marshmallow_enum import EnumField
from ... import ma
from ..WagerStatus import WagerStatus
from ...common import WagerStatusEnum


class WagerStatusSchema(ma.SQLAlchemySchema):
    name = EnumField(WagerStatusEnum)

    class Meta:
        model = WagerStatus
        load_instance = True

    uuid = ma.auto_field()
