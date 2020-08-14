from sqlalchemy_utils import UUIDType
from .. import db
from .mixins import BaseMixin


class Contest(db.Model, BaseMixin):
    contest_uuid = db.Column(UUIDType(binary=False), nullable=False)

    # FK
    wager_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('wager.uuid'), nullable=False)

    # Relationship
    wager = db.relationship("Wager")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Contest.register()
