from marshmallow import Schema, post_dump
from marshmallow_enum import EnumField
from webargs import fields
from ....common import ParticipantStatusEnum
from ..parties.schema import DumpSchema as DumpPartySchema
import logging


class CreateSchema(Schema):
    user_uuid = fields.UUID(required=True)
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    party = fields.Nested(DumpPartySchema)


class DumpSchema(Schema):
    status = EnumField(ParticipantStatusEnum)
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    user_uuid = fields.UUID()
    party = fields.Nested(DumpPartySchema)

    def get_attribute(self, obj, attr, default):
        if attr == 'party':
            return getattr(obj, attr, default) if any(
                attr in expand for expand in self.context.get('expand', [])) else None
        else:
            return getattr(obj, attr, default)

    @post_dump
    def make_obj(self, data, **kwargs):
        if data.get('party', False) is None:
            del data['party']
        return data


class FetchAllSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    expand = fields.DelimitedList(fields.String(), required=False, missing=[])
    user_uuid = fields.UUID(required=False)


create_schema = CreateSchema()
dump_schema = DumpSchema()
dump_many_schema = DumpSchema(many=True)
fetch_all_schema = FetchAllSchema()
