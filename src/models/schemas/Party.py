from ... import ma
from ..Party import Party


class PartySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Party
        load_instance = True

    uuid = ma.auto_field()
