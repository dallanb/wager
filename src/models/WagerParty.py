from ..common import WagerStatusEnum
from .. import db
from .mixins import BaseMixin
from .utils import generate_hash


class WagerParty(db.Model, BaseMixin):
    hash = db.Column(db.BigInteger, nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def hash_members(members):
        return generate_hash(members)


WagerParty.register()
