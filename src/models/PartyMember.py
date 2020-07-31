from sqlalchemy_utils import UUIDType, generic_repr
from .. import db, ma
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


class PartyMemberSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PartyMember
        load_instance = True

    uuid = ma.auto_field()
    member = ma.auto_field()



PartyMember.register()
