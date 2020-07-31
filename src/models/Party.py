from sqlalchemy_utils import generic_repr
from .. import db, ma
from .mixins import BaseMixin


@generic_repr('id', 'uuid')
class Party(db.Model, BaseMixin):
    hash = db.Column(db.BigInteger, nullable=False, unique=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PartySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Party
        load_instance = True

    uuid = ma.auto_field()
Party.register()
