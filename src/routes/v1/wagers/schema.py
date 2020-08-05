from marshmallow import fields, validate, Schema
from marshmallow_enum import EnumField
from ....common import ParticipantStatusEnum


class CreateSchema(Schema):
    contest_uuid = fields.UUID()


class DumpSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    owner_uuid = fields.UUID()
    status = EnumField(ParticipantStatusEnum)


class FetchAllSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)


create_schema = CreateSchema()
dump_schema = DumpSchema()
dump_many_schema = DumpSchema(many=True)
fetch_all_schema = FetchAllSchema()
