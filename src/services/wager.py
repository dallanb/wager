from flask import g
from .base import Base
from .course import Course
from .party import Party
from .stake import Stake
from .wager_status import WagerStatus
from ..models import Wager as WagerModel, WagerSchema
from ..common import WagerStatusEnum, advanced_query
from .. import cache


class Wager(Base):
    def __init__(self):
        super().__init__()
        self.logger = g.logger.getLogger(__name__)

    @staticmethod
    def assign_course(**kwargs):
        course = kwargs.get("course", None)

        if course is not None:
            courses = Course.find_course(uuid=course)
            if not courses:
                raise ValueError('Invalid course')
            course = courses[0]
        return course

    @staticmethod
    def assign_owner(**kwargs):
        return g.user

    @staticmethod
    def assign_party(**kwargs):
        members = kwargs.get("members", None)

        party = None
        if members is not None:
            parties = Party.find_party_by_members(members=members)
            if not parties:
                party = Party.create_party_by_members(members=members)
            else:
                party = parties[0]
        return party

    @staticmethod
    def assign_stake(**kwargs):
        uuid = kwargs.get("uuid", None)
        currency = kwargs.get("currency", None)
        amount = kwargs.get("amount", None)

        stake = None
        if currency is not None or amount is not None:
            if uuid is None:
                stake = Stake.create_stake(currency=currency, amount=amount)
            else:
                stake = Stake.update_stake(uuid=uuid, currency=currency, amount=amount)

        return stake

    @staticmethod
    def assign_status(**kwargs):
        return WagerStatus.find_status(status_enum=WagerStatusEnum.active)

    @staticmethod
    def assign_time(**kwargs):
        return kwargs.get("time", None)

    @cache.memoize(timeout=10)
    def find_wager(self, uuid=None):
        filters = []
        if uuid:
            filters.append(('equal', [('uuid', uuid)]))

        wagers = advanced_query(model=WagerModel, filters=filters)
        self.logger.info(wagers)
        return wagers

    @classmethod
    def create_wager(cls, **kwargs):
        wager = WagerModel()

        # add owner
        wager.owner = cls.assign_owner(**kwargs)

        # add status
        wager.status = cls.assign_status(**kwargs)

        # add party
        wager.party = cls.assign_party(**kwargs)

        # add time
        wager.time = cls.assign_time(**kwargs)

        # add take
        wager.stake = cls.assign_stake(**kwargs)

        # add course
        wager.course = cls.assign_course(**kwargs)

        g.db.session.add(wager)
        g.db.session.commit()

        return wager

    @classmethod
    def update_wager(cls, uuid, **kwargs):
        # find wager by uuid
        wagers = cls.find_wager(uuid)
        if not wagers:
            raise ValueError('Invalid UUID')

        # def __repr__(self):
        #         return "%s(%s)" % (self.__class__.__name__, self.id)

        wager = wagers[0]

        # validation
        if kwargs.get('members') is not None and wager.party is not None:
            raise ValueError('Members cannot be updated once set')

        # update time
        time = cls.assign_time(**kwargs)
        if time is not None:
            wager.time = time

        # update stake
        stake = cls.assign_stake(uuid=wager.stake_uuid, **kwargs)
        if stake is not None:
            wager.stake = stake

        # update course
        course = cls.assign_course(**kwargs)
        if course is not None:
            wager.course = course

        # update party
        party = cls.assign_party(**kwargs)
        if party is not None:
            wager.party = party

        g.db.session.commit()
        return wager

    @classmethod
    def destroy_wager(cls, uuid):
        wagers = cls.find_wager(uuid)
        if not wagers:
            raise ValueError('Invalid UUID')

        wager = wagers[0]

        g.db.session.delete(wager)
        g.db.session.commit()
        return True

    @staticmethod
    def dump_wager(wager, **kwargs):
        return WagerSchema().dump(wager, **kwargs)
