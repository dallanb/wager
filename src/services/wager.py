from flask import g
from .base import Base
from .course import Course
from .party import Party
from .stake import Stake
from .wager_status import WagerStatus
from ..models import Wager as WagerModel, WagerSchema
from ..common import WagerStatusEnum, advanced_query, is_mapped, is_uuid
from .. import cache, db


class Wager(Base):
    def __init__(self):
        super().__init__()
        self.logger = g.logger.getLogger(__name__)

    @staticmethod
    def assign_course(**kwargs):
        course = kwargs.get("course", None)

        if not course:
            return None

        if is_mapped(course):
            return course
        elif is_uuid(course):
            courses = Course.find_course(uuid=course)
            if not courses:
                raise ValueError('Invalid course')
            return courses[0]
        else:
            raise TypeError('Invalid course')

    @staticmethod
    def assign_owner(**kwargs):
        return g.user

    @staticmethod
    def assign_party(**kwargs):
        members = kwargs.get("members", None)
        party = kwargs.get("party", None)

        if is_mapped(party):
            return party
        elif is_uuid(party):
            parties = Party.find_party(uuid=party)
            if not parties:
                raise ValueError('Invalid party')
            return parties[0]
        elif not party:
            if members is not None:
                parties = Party.find_party_by_members(members=members)
                if not parties:
                    return Party.create_party_by_members(members=members)
                else:
                    return parties[0]
        else:
            raise TypeError('Invalid party')

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
        status = kwargs.get("status", WagerStatusEnum.active)
        return WagerStatus.find_status(status_enum=status)

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
        wager = WagerModel(**kwargs)
        return wager

    @classmethod
    def save_wager(cls, wager):
        if not is_mapped(wager):
            raise ValueError('Invalid wager')

        if not wager.pending:
            db.session.add(wager)

        db.session.commit(wager)
        return wager

    @classmethod
    def destroy_wager(cls, uuid):
        wagers = cls.find_wager(uuid)
        if not wagers:
            raise ValueError('Invalid UUID')

        wager = wagers[0]

        db.session.delete(wager)
        db.session.commit()
        return True

    @staticmethod
    def dump_wager(wager, **kwargs):
        return WagerSchema().dump(wager, **kwargs)
