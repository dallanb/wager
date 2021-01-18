from sqlalchemy_utils import UUIDType

from .mixins import BaseMixin
from .. import db


class Contest(db.Model, BaseMixin):
    buy_in = db.Column(db.Float)
    contest_uuid = db.Column(UUIDType(binary=False), nullable=False)
    # FK
    wager_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('wager.uuid'), nullable=False)

    # Relationship
    wager = db.relationship("Wager")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Contest.register()
