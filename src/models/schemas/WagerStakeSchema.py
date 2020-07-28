from marshmallow_enum import EnumField
from ... import ma
from ..WagerStake import WagerStake


class WagerStakeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = WagerStake
        load_instance = True

    uuid = ma.auto_field()
    balance = ma.auto_field()