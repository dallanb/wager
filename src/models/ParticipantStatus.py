from ..common import ParticipantStatusEnum
from .. import db
from .mixins import StatusMixin


class ParticipantStatus(db.Model, StatusMixin):
    name = db.Column(db.Enum(ParticipantStatusEnum), primary_key=True, unique=True, nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


ParticipantStatus.register()
