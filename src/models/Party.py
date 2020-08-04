from sqlalchemy_utils import generic_repr, UUIDType
from .. import db, ma
from ..models import Wager
from .mixins import BaseMixin


@generic_repr('id', 'uuid')
class Party(db.Model, BaseMixin):
    name = db.Column(db.String, nullable=False, unique=True)

    # FK
    wager_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('wager.uuid'), nullable=False)

    # Relationship
    wager = db.relationship("Wager")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PartySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Party
        load_instance = True

    uuid = ma.auto_field()
    name = ma.auto_field()


Party.register()
