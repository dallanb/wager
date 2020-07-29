from flask import g
from .base import Base
from ..models import PartyMember as PartyMemberModel


class PartyMember(Base):
    def __init__(self):
        super().__init__()
        self.logger = g.logger.getLogger(__name__)

    @staticmethod
    def create_members(members, party):
        party_members = []
        for member in members:
            party_member = PartyMemberModel(member=member, party=party)
            party_members.append(party_member)
            g.db.session.add(party_member)
        g.db.session.commit()
        return party_members
