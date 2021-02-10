from sqlalchemy.orm import validates
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

    @validates('wager_uuid')
    def validates_wager_uuid(self, key, value):
        if self.wager_uuid:  # Field already exists
            raise ValueError('wager_uuid cannot be modified.')

        return value

    @validates('wager')
    def validates_party(self, key, value):
        if self.wager:  # Field already exists
            raise ValueError('wager cannot be modified.')

        return value


Party.register()
