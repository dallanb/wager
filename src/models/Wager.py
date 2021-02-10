import logging

from sqlalchemy.orm import validates

from .mixins import BaseMixin
from .. import db
from ..common import WagerStatusEnum


class Wager(db.Model, BaseMixin):
    # FK
    status = db.Column(db.Enum(WagerStatusEnum), db.ForeignKey('wager_status.name'), nullable=False,
                       default=WagerStatusEnum['pending'])

    # Relationship
    wager_status = db.relationship("WagerStatus")
    parties = db.relationship("Party", back_populates='wager')
    payouts = db.relationship("Payout", back_populates='wager')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @validates('status')
    def validates_status(self, key, value):
        logging.info(self.status)
        logging.info(value)
        # if self.status != value:
        #     if self.status
        # if self.rank:  # Field already exists
        #     raise ValueError('rank cannot be modified.')

        return value


Wager.register()
