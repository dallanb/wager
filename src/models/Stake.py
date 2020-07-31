from sqlalchemy_utils import CurrencyType, generic_repr
from .. import db, ma
from .mixins import BaseMixin


@generic_repr('id', 'uuid')
class Stake(db.Model, BaseMixin):
    currency = db.Column(CurrencyType)
    amount = db.Column(db.Integer)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class StakeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Stake
        load_instance = True

    uuid = ma.auto_field()
    currency = ma.auto_field()
    amount = ma.auto_field()

Stake.register()
