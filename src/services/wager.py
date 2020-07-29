from flask import g
from .base import Base
from .party import Party
from .stake import Stake
from .wager_status import WagerStatus
from ..models import Wager as WagerModel, WagerSchema
from ..common import WagerStatusEnum, advanced_query


class Wager(Base):
    def __init__(self):
        super().__init__()
        self.logger = g.logger.getLogger(__name__)

    @staticmethod
    def find_wager(uuid=None):
        filters = []
        if uuid:
            filters.append(('equal', [('uuid', uuid)]))

        wagers = advanced_query(model=WagerModel, filters=filters)
        return wagers

    @classmethod
    def create_wager(cls, **kwargs):
        members = kwargs.get("members", [])

        wager = WagerModel()

        # add owner
        wager.owner = g.user

        # add status
        wager.status = WagerStatus.find_status(status_enum=WagerStatusEnum.active)

        # add party
        parties = Party.find_party_by_members(members=members)
        if not parties:
            wager.party = Party.create_party_by_members(members=members)
        else:
            wager.party = parties[0]

        g.db.session.add(wager)
        g.db.session.commit()

        return wager

    @classmethod
    def update_wager(cls, uuid, **kwargs):
        time = kwargs.get("time", None)
        currency = kwargs.get("currency", None)
        amount = kwargs.get("amount", None)
        course = kwargs.get("course", None)
        members = kwargs.get("members", None)

        wagers = cls.find_wager(uuid)
        if not wagers:
            raise Exception('Invalid UUID')

        wager = wagers[0]

        if time is not None:
            wager.time = time

        if currency is not None or amount is not None:
            if wager.stake is None:
                wager.stake = Stake.create_stake(currency=currency, amount=amount)
            else:
                wager.stake = Stake.update_stake(uuid=wager.stake_uuid, currency=currency, amount=amount)

        if course is not None:
            wager.course = course

        if members is not None:
            if wager.party is not None:
                raise Exception('Members cannot be updated once set')
            wager.party = Party.create_party_by_members(members=members)

        g.db.session.commit()
        return wager

    @classmethod
    def destroy_wager(cls, uuid):
        wagers = cls.find_wager(uuid)
        if not wagers:
            raise Exception('Invalid UUID')

        wager = wagers[0]

        g.db.session.delete(wager)
        g.db.session.commit()
        return True

    @staticmethod
    def dump_wager(wager, **kwargs):
        return WagerSchema().dump(wager, **kwargs)
