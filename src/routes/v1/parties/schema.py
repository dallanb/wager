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
    wager = fields.Nested(DumpWagerSchema)

    def get_attribute(self, obj, attr, default):
        if attr == 'wager':
            logging.info(self.context.get('expand', []))
            return getattr(obj, attr, default) if any(
                attr in expand for expand in self.context.get('expand', [])) else None
        else:
            return getattr(obj, attr, default)

    @post_dump
    def make_obj(self, data, **kwargs):
        if data.get('wager', False) is None:
            del data['wager']
        return data


class FetchAllSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    expand = fields.DelimitedList(fields.String(), required=False, missing=[])


class UpdateSchema(Schema):
    name = fields.String(required=True)


create_schema = CreateSchema()
dump_schema = DumpSchema()
dump_many_schema = DumpSchema(many=True)
fetch_all_schema = FetchAllSchema()
update_schema = UpdateSchema()
