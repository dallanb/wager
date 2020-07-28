from ..common import WagerStatusEnum
from .. import db
from .mixins import BaseMixin


class WagerStatus(db.Model, BaseMixin):
    name = db.Column(db.Enum(WagerStatusEnum), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


WagerStatus.register()
