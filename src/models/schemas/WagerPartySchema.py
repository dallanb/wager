from marshmallow_enum import EnumField
from ... import ma
from ..WagerParty import WagerParty


class WagerPartySchema(ma.SQLAlchemySchema):
    class Meta:
        model = WagerParty
        load_instance = True

    uuid = ma.auto_field()
