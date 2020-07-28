from marshmallow_enum import EnumField
from ... import ma
from ..WagerCourse import WagerCourse


class WagerCourseSchema(ma.SQLAlchemySchema):

    class Meta:
        model = WagerCourse
        load_instance = True

    uuid = ma.auto_field()
    golf_canada_id = ma.auto_field()
