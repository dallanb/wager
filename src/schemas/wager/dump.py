from marshmallow import fields, validate, Schema
from marshmallow_enum import EnumField
from ...common import ParticipantStatusEnum


class DumpSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    owner_uuid = fields.UUID()
    status = EnumField(ParticipantStatusEnum)


dump_schema = DumpSchema()
dump_many_schema = DumpSchema(many=True)
