from marshmallow import fields, validate, Schema
from sqlalchemy_utils import CurrencyType
from src.schemas.participant.dump import DumpSchema as DumpParticipantSchema


class DumpSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    currency = CurrencyType()
    amount = fields.String()
    participant = fields.Nested(DumpParticipantSchema)


dump_schema = DumpSchema()
dump_many_schema = DumpSchema(many=True)
