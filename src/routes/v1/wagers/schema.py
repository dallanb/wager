from marshmallow import validate, Schema, post_dump
from webargs import fields
from marshmallow_enum import EnumField
from ....common import ParticipantStatusEnum

class DumpWagerSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    status = EnumField(ParticipantStatusEnum)
    parties = fields.List(fields.Nested('DumpPartySchema', exclude=('wager',)))

    def get_attribute(self, obj, attr, default):
        if attr == 'parties':
            return getattr(obj, attr, default) if any(
                attr in include for include in self.context.get('include', [])) else None
        else:
            return getattr(obj, attr, default)

    @post_dump
    def make_obj(self, data, **kwargs):
        if data.get('parties', False) is None:
            del data['parties']
        return data


class FetchAllWagerSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    include = fields.DelimitedList(fields.String(), required=False, missing=[])


dump_schema = DumpWagerSchema()
dump_many_schema = DumpWagerSchema(many=True)
fetch_all_schema = FetchAllWagerSchema()
