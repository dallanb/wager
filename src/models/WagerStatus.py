from ..common import WagerStatusEnum
from .. import db
from .mixins import StatusMixin


class WagerStatus(db.Model, StatusMixin):
    name = db.Column(db.Enum(WagerStatusEnum), primary_key=True, unique=True, nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


WagerStatus.register()
