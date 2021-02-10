from sqlalchemy.orm import validates
from sqlalchemy_utils import UUIDType

from .mixins import BaseMixin
from .. import db


class Contest(db.Model, BaseMixin):
    buy_in = db.Column(db.Float, default=0.0)
    contest_uuid = db.Column(UUIDType(binary=False), nullable=False, unique=True)
    # FK
    wager_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('wager.uuid'), nullable=False)

    # Relationship
    wager = db.relationship("Wager", lazy="joined")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @validates('buy_in')
    def validates_buy_in(self, key, value):
        if self.buy_in:  # Field already exists
            raise ValueError('buy_in cannot be modified.')

        return value


Contest.register()
