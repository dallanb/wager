from sqlalchemy_utils import UUIDType

from .mixins import BaseMixin
from .. import db
from ..common import WagerStatusEnum


class Wager(db.Model, BaseMixin):
    # FK
    status = db.Column(db.Enum(WagerStatusEnum), db.ForeignKey('wager_status.name'), nullable=False,
                       default=WagerStatusEnum['pending'])
    contest_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('contest.uuid'), nullable=False)

    # Relationship
    wager_status = db.relationship("WagerStatus")
    parties = db.relationship("Party", back_populates='wager')
    payouts = db.relationship("Payout", back_populates='wager')
    contest = db.relationship("Contest")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Wager.register()
