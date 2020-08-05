from sqlalchemy_utils import generic_repr, UUIDType
from .. import db
from ..models.Wager import Wager
from .mixins import BaseMixin


class Party(db.Model, BaseMixin):
    name = db.Column(db.String, nullable=False, unique=True)

    # FK
    wager_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('wager.uuid'), nullable=False)

    # Relationship
    wager = db.relationship("Wager", lazy='joined')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Party.register()
