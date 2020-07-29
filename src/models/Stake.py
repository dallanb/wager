from sqlalchemy_utils import CurrencyType, generic_repr
from .. import db
from .mixins import BaseMixin


@generic_repr('id', 'uuid')
class Stake(db.Model, BaseMixin):
    currency = db.Column(CurrencyType)
    amount = db.Column(db.Integer)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Stake.register()
