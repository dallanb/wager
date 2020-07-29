from ... import ma
from ..Course import Course


class CourseSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Course
        load_instance = True

    uuid = ma.auto_field()
    golf_canada_id = ma.auto_field()
