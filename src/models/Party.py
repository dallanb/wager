from sqlalchemy_utils import generic_repr
from .. import db
from .mixins import BaseMixin


@generic_repr('id', 'uuid')
class Party(db.Model, BaseMixin):
    hash = db.Column(db.BigInteger, nullable=False, unique=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Party.register()
