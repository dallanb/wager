from .. import db
from .mixins import BaseMixin


class WagerCourse(db.Model, BaseMixin):
    golf_canada_id = db.Column(db.Integer, nullable=False)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


WagerCourse.register()
