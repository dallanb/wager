from sqlalchemy_utils import generic_repr
from ..common import WagerStatusEnum
from .. import db
from .mixins import BaseMixin


@generic_repr('id', 'uuid')
class WagerStatus(db.Model, BaseMixin):
    name = db.Column(db.Enum(WagerStatusEnum), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


WagerStatus.register()
