from sqlalchemy_utils import UUIDType

from .mixins import BaseMixin
from .. import db


class Payout(db.Model, BaseMixin):
    rank = db.Column(db.Integer, nullable=False)
    proportion = db.Column(db.Float, nullable=False)
    # FK
    wager_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('wager.uuid'), nullable=False)

    # Relationship
    wager = db.relationship("Wager")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Payout.register()
