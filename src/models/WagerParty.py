from ..common import WagerStatusEnum
from .. import db
from .mixins import BaseMixin


class WagerParty(db.Model, BaseMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



WagerParty.register()
