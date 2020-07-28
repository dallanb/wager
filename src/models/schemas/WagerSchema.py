from ... import ma
from ..Wager import Wager


class WagerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Wager
        load_instance = True

    uuid = ma.auto_field()
    time = ma.auto_field()
    owner = ma.auto_field()
    stake_uuid = ma.auto_field()
    party_uuid = ma.auto_field()
    course_uuid = ma.auto_field()
    status_uuid = ma.auto_field()
