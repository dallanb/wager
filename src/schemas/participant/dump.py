from marshmallow import fields, Schema
from marshmallow_enum import EnumField
from ...common import ParticipantStatusEnum
from src.schemas.party.dump import DumpSchema as DumpPartySchema


class DumpSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    party = fields.Nested(DumpPartySchema)
    user_uuid = fields.UUID()
    status = EnumField(ParticipantStatusEnum)


dump_schema = DumpSchema()
dump_many_schema = DumpSchema(many=True)
