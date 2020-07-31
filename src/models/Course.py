from sqlalchemy_utils import generic_repr
from .. import db, ma
from .mixins import BaseMixin


@generic_repr('id', 'uuid')
class Course(db.Model, BaseMixin):
    golf_canada_id = db.Column(db.Integer, unique=True, nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CourseSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Course
        load_instance = True

    uuid = ma.auto_field()
    golf_canada_id = ma.auto_field()

Course.register()
