from sqlalchemy_utils import CompositeType, CurrencyType
from .. import db
from .mixins import BaseMixin


class WagerStake(db.Model, BaseMixin):
    balance = db.Column(
        CompositeType(
            'money_type',
            [
                db.Column('currency', CurrencyType),
                db.Column('amount', db.Integer)
            ]
        )
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


WagerStake.register()
