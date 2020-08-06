from sqlalchemy_utils import generic_repr, UUIDType
from .. import db
from .mixins import BaseMixin


class Party(db.Model, BaseMixin):
    name = db.Column(db.String, nullable=False, unique=True)

    # FK
    wager_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('wager.uuid'), nullable=False)

    # Relationship
    wager = db.relationship("Wager", back_populates="parties", lazy="noload")
    participants = db.relationship("Participant", back_populates="party", lazy="noload")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Party.register()
