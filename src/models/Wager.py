from sqlalchemy_utils import UUIDType, generic_repr
from .. import db
from .mixins import BaseMixin


@generic_repr('id', 'uuid')
class Wager(db.Model, BaseMixin):
    owner = db.Column(UUIDType(binary=False), nullable=False)
    time = db.Column(db.BigInteger, nullable=True)

    # FK
    stake_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('stake.uuid'), nullable=True)
    party_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('party.uuid'), nullable=True)
    course_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('course.uuid'), nullable=True)
    status_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('wager_status.uuid'), nullable=True)

    # Relationship
    stake = db.relationship("Stake", cascade="all, delete")
    party = db.relationship("Party")
    course = db.relationship("Course")
    status = db.relationship("WagerStatus")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Wager.register()
