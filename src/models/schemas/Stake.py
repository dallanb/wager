from ... import ma
from ..Stake import Stake


class StakeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Stake
        load_instance = True

    uuid = ma.auto_field()
    currency = ma.auto_field()
    amount = ma.auto_field()
