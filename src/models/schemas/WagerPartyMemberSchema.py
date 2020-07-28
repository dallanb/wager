from marshmallow_enum import EnumField
from ... import ma
from ..WagerPartyMember import WagerPartyMember


class WagerPartyMemberSchema(ma.SQLAlchemySchema):
    class Meta:
        model = WagerPartyMember
        load_instance = True

    uuid = ma.auto_field()
    member_uuid = ma.auto_field()
