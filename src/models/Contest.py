from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import validates
from sqlalchemy_utils import UUIDType

from .. import db
from ..common import time_now, camel_to_snake


# This is almost a materialized model
class Contest(db.Model):
    @declared_attr
    def __tablename__(cls):
        return camel_to_snake(cls.__name__)

    contest_uuid = db.Column(UUIDType(binary=False), primary_key=True, unique=True,
                             nullable=False)  # this is the contest uuid from the Contest SERVICE
    ctime = db.Column(db.BigInteger, default=time_now)
    mtime = db.Column(db.BigInteger, onupdate=time_now)
    buy_in = db.Column(db.Float, default=0.0)

    # Relationship
    wager = db.relationship("Wager", uselist=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @validates('buy_in')
    def validates_buy_in(self, key, value):
        if self.buy_in:  # Field already exists
            raise ValueError('buy_in cannot be modified.')

        return value
