from flask import g
from .base import Base
from .party_member import PartyMember
from ..models import Party as PartyModel
from ..common import generate_hash, advanced_query
from .. import cache, db


class Party(Base):
    def __init__(self):
        super().__init__()
        self.logger = g.logger.getLogger(__name__)

    @staticmethod
    @cache.memoize(10)
    def hash_members(members):
        return generate_hash(members)

    @staticmethod
    @cache.memoize(10)
    def find_party_by_hash(party_hash):
        if not party_hash:
            raise ValueError('Missing hash')

        filters = [('equal', [('hash', party_hash)])]
        parties = advanced_query(model=PartyModel, filters=filters)
        return parties

    @classmethod
    @cache.memoize(10)
    def find_party_by_members(cls, members):
        if not members:
            return ValueError('Missing members')

        # find hash for party
        party_hash = cls.hash_members(members)

        parties = cls.find_party_by_hash(party_hash)
        return parties

    @staticmethod
    @cache.memoize(10)
    def find_party(uuid=None):
        filters = []
        if uuid is not None:
            filters.append(('equal', [('uuid', uuid)]))

        parties = advanced_query(model=PartyModel, filters=filters)
        return parties

    @staticmethod
    def create_party(**kwargs):
        party = PartyModel(**kwargs)
        db.session.add(party)
        db.session.commit()
        return party

    @classmethod
    def create_party_by_members(cls, members):
        if members is None:
            raise ValueError('Missing members')

        hash_members = cls.hash_members(members)
        party = cls.create_party(hash=hash_members)
        members = PartyMember.create_party_member(members=members, party=party)
        return party
