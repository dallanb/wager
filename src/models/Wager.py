from .mixins import BaseMixin
from .. import db
from ..common import WagerStatusEnum


class Wager(db.Model, BaseMixin):
    # FK
    status = db.Column(db.Enum(WagerStatusEnum), db.ForeignKey('wager_status.name'), nullable=True)

    # Relationship
    wager_status = db.relationship("WagerStatus")
    parties = db.relationship("Party", back_populates='wager', lazy="noload")
    payouts = db.relationship("Payout", back_populates='wager', lazy="noload")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Wager.register()
