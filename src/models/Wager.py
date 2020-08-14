from sqlalchemy_utils import UUIDType
from .. import db
from ..common import WagerStatusEnum
from .mixins import BaseMixin


class Wager(db.Model, BaseMixin):
    owner_uuid = db.Column(UUIDType(binary=False), nullable=False)

    # FK
    status = db.Column(db.Enum(WagerStatusEnum), db.ForeignKey('wager_status.name'), nullable=True)

    # Relationship
    wager_status = db.relationship("WagerStatus")
    parties = db.relationship("Party", back_populates='wager', lazy="noload")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Wager.register()
