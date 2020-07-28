from .flask import g
from .base import Base
from ..models import WagerModel, WagerSchema, WagerPartyModel, WagerPartyMemberModel
from ..common import WagerStatusEnum


class Wager(Base):
    def __init__(self):
        self.logger = g.logger.getLogger(__name__)

    @staticmethod
    def find_status(status):
        return WagerModel.find_status(status)

    @classmethod
    def find_party(cls, members):
        if members is None:
            return None

        # find hash for party
        party_hash = WagerPartyModel.hash_members(members)

        party = WagerPartyModel.query.filter(WagerPartyModel.hash == party_hash).first()
        if party:
            return party

        party = cls.create_party(hash=party_hash)
        members = cls.create_members(members, party)
        return party

    @staticmethod
    def create_party(**kwargs):
        party = WagerPartyMemberModel(*kwargs)
        g.db.session.add(party)
        g.db.session.commit()
        return party

    @staticmethod
    def create_members(members, party):
        party_members = []
        for member in members:
            party_member = WagerPartyMemberModel(member=member, party=party)
            party_members.append(party_member)
            g.db.session.add(party_member)
        g.db.session.commit()
        return party_members

    @classmethod
    def create_wager(cls, **kwargs):
        members = kwargs.get("members", [])

        wager = Wager()

        # add owner
        wager.owner = g.user

        # add status
        wager.status = cls.find_status(WagerStatusEnum.active)

        # add party
        wager.party = cls.find_party(members=members)

        g.db.session.add(wager)
        g.db.session.commit()

    @staticmethod
    def dump_wager(wager):
        return WagerSchema().dump(wager)
