from sqlalchemy_utils import generic_repr
from .. import db
from .mixins import BaseMixin


@generic_repr('id', 'uuid')
class Course(db.Model, BaseMixin):
    golf_canada_id = db.Column(db.Integer, unique=True, nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Course.register()
