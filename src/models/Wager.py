from sqlalchemy_utils import UUIDType, generic_repr
from .. import db, ma
from ..models import Course, Party, Stake, WagerStatus
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


class WagerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Wager
        load_instance = True

    uuid = ma.auto_field()
    time = ma.auto_field()
    owner = ma.auto_field()
    stake_uuid = ma.auto_field()
    party_uuid = ma.auto_field()
    course_uuid = ma.auto_field()
    status_uuid = ma.auto_field()


Wager.register()
