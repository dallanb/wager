from flask import g
from .base import Base
from ..models import PartyMember as PartyMemberModel
from ..common import advanced_query
from .. import cache


class PartyMember(Base):
    def __init__(self):
        super().__init__()
        self.logger = g.logger.getLogger(__name__)

    @staticmethod
    @cache.memoize(10)
    def find_party_member(uuid=None):
        filters = []
        if uuid:
            filters.append(('equal', [('uuid', uuid)]))

        members = advanced_query(model=PartyMemberModel, filters=filters)
        return members

    @staticmethod
    def create_party_member(members, party):
        if not members:
            raise ValueError('Missing members')

        party_members = []
        for member in members:
            party_member = PartyMemberModel(member=member, party=party)
            party_members.append(party_member)
            g.db.session.add(party_member)
        g.db.session.commit()
        return party_members
