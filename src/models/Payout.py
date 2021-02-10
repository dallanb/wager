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
    wager = db.relationship("Wager", lazy="joined")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @validates('rank')
    def validates_rank(self, key, value):
        if self.rank:  # Field already exists
            raise ValueError('rank cannot be modified.')

        return value

    @validates('proportion')
    def validates_proportion(self, key, value):
        if value > 1.0:
            raise ValueError('proportion cannot be greater that 1.0.')
        elif value < 0.0:
            raise ValueError('proportion cannot be less than 0.0.')

        if self.proportion:  # Field already exists
            raise ValueError('proportion cannot be modified.')

        return value


Payout.register()
