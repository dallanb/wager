from sqlalchemy_utils import UUIDType, generic_repr
from marshmallow_enum import EnumField
from .. import db, ma
from ..models import WagerStatus
from ..common import WagerStatusEnum
from .mixins import BaseMixin


@generic_repr('id', 'uuid')
class Wager(db.Model, BaseMixin):
    owner_uuid = db.Column(UUIDType(binary=False), nullable=False)

    # FK
    status = db.Column(db.Enum(WagerStatusEnum), db.ForeignKey('wager_status.name'), nullable=True)

    # Relationship
    wager_status = db.relationship("WagerStatus")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class WagerSchema(ma.SQLAlchemySchema):
    status = EnumField(WagerStatusEnum)

    class Meta:
        model = Wager
        load_instance = True

    uuid = ma.auto_field()
    ctime = ma.auto_field()
    mtime = ma.auto_field()
    owner_uuid = ma.auto_field()


Wager.register()
