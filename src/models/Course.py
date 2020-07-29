from .. import db
from .mixins import BaseMixin


class Course(db.Model, BaseMixin):
    golf_canada_id = db.Column(db.Integer, nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Course.register()
