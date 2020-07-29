from ... import ma
from ..PartyMember import PartyMember


class PartyMemberSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PartyMember
        load_instance = True

    uuid = ma.auto_field()
    member = ma.auto_field()
