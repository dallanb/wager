from marshmallow import validate, Schema, post_load, post_dump
from webargs import fields
from ..wagers.schema import DumpSchema as DumpWagerSchema
import logging


class CreateSchema(Schema):
    name = fields.String(required=True)


class DumpSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    name = fields.String()
    wager = fields.Nested(DumpWagerSchema(only=["uuid"]))

    def get_attribute(self, obj, attr, default):
        if attr == 'wager':
            return getattr(obj, attr, default) if attr in self.context.get('expand', []) else None
        else:
            return getattr(obj, attr, default)

    @post_dump
    def make_obj(self, data, **kwargs):
        if not data['wager']:
            del data['wager']
        return data


class FetchAllSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    expand = fields.DelimitedList(fields.String(), required=False)


class UpdateSchema(Schema):
    name = fields.String(required=True)


create_schema = CreateSchema()
dump_schema = DumpSchema()
dump_many_schema = DumpSchema(many=True)
fetch_all_schema = FetchAllSchema()
update_schema = UpdateSchema()
