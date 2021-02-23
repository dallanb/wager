from sqlalchemy.orm import validates
from sqlalchemy_utils import UUIDType

from .mixins import BaseMixin
from .. import db


class Payout(db.Model, BaseMixin):
    # Constraints
    __table_args__ = (db.UniqueConstraint('rank', 'wager_uuid', name='wager_rank'),)

    rank = db.Column(db.Integer, nullable=False)
    proportion = db.Column(db.Float, nullable=False)
    # FK
    wager_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('wager.uuid'), nullable=False)

    # Relationship
    wager = db.relationship("Wager", back_populates='payouts', lazy="joined")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @validates('proportion')
    def validates_proportion(self, key, value):
        if value > 1.0:
            raise ValueError('proportion cannot be greater that 1.0.')
        elif value < 0.0:
            raise ValueError('proportion cannot be less than 0.0.')
        return value


Payout.register()
