from sqlalchemy_utils import CurrencyType
from .. import db
from .mixins import BaseMixin


class Stake(db.Model, BaseMixin):
    currency = db.Column(CurrencyType)
    amount = db.Column(db.Integer)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Stake.register()
