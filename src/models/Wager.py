from sqlalchemy_utils import EmailType, PasswordType, UUIDType
from .. import db
from .mixins import BaseMixin
from .WagerStatus import WagerStatus


class Wager(db.Model, BaseMixin):
    time = db.Column(db.BigInteger)
    owner = db.Column(UUIDType(binary=False))

    # FK
    stake_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('wager_stake.uuid'), nullable=True)
    party_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('wager_party.uuid'), nullable=True)
    course_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('wager_course.uuid'), nullable=True)
    status_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('wager_status.uuid'), nullable=True)

    # Relationship
    stake = db.relationship("WagerStake")
    party = db.relationship("WagerParty")
    course = db.relationship("WagerCourse")
    status = db.relationship("WagerStatus")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    @staticmethod
    def find_status(status_enum=None):
        if status_enum is None:
            return None

        status = WagerStatus.query.filter(WagerStatus.name == status_enum).first()

        if status_enum is None:
            return None

        return status


Wager.register()
