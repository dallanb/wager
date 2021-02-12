from sqlalchemy_utils import UUIDType

from .mixins import BaseMixin
from .. import db


class Party(db.Model, BaseMixin):
    # FK
    wager_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('wager.uuid'), nullable=False)

    # Relationship
    wager = db.relationship("Wager", back_populates="parties")
    participants = db.relationship("Participant", back_populates="party")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Party.register()
