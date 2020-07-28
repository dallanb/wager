from sqlalchemy_utils import UUIDType
from .. import db
from .mixins import BaseMixin


class WagerPartyMember(db.Model, BaseMixin):
    member = db.Column(UUIDType(binary=False), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # FK
    wager_party_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('wager_party.uuid'), nullable=False)

    # Relationship
    party = db.relationship("WagerParty")


WagerPartyMember.register()
