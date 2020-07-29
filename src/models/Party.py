from .. import db
from .mixins import BaseMixin


class Party(db.Model, BaseMixin):
    hash = db.Column(db.BigInteger, nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Party.register()
