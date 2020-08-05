from marshmallow import fields, Schema
from marshmallow_enum import EnumField
from ....common import ParticipantStatusEnum
from ..parties.schema import DumpSchema as DumpPartySchema


class CreateSchema(Schema):
    user_uuid = fields.UUID(required=True)
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    party = fields.Nested(DumpPartySchema)
    user_uuid = fields.UUID()


class DumpSchema(Schema):
    status = EnumField(ParticipantStatusEnum)
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()


class FetchAllSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)


create_schema = CreateSchema()
dump_schema = DumpSchema()
dump_many_schema = DumpSchema(many=True)
fetch_all_schema = FetchAllSchema()
