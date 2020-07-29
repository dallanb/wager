from sqlalchemy_utils import UUIDType, generic_repr
from .. import db
from .mixins import BaseMixin


@generic_repr('id', 'uuid')
class PartyMember(db.Model, BaseMixin):
    member = db.Column(UUIDType(binary=False), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # FK
    wager_party_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('party.uuid'), nullable=False)

    # Relationship
    party = db.relationship("Party")


PartyMember.register()
