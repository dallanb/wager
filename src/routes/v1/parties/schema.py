from marshmallow import validate, Schema, post_load, post_dump
from webargs import fields


class CreatePartySchema(Schema):
    name = fields.String(required=True)


class DumpPartySchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    name = fields.String()
    wager = fields.Nested('DumpWagerSchema', only=("uuid", "ctime", "mtime", "status", "owner_uuid"))
    participants = fields.List(fields.Nested('DumpParticipantSchema', exclude=('party',)))

    def get_attribute(self, obj, attr, default):
        if attr == 'wager':
            return getattr(obj, attr, default) if any(
                attr in expand for expand in self.context.get('expand', [])) else None
        if attr == 'participants':
            return getattr(obj, attr, default) if any(
                attr in include for include in self.context.get('include', [])) else None
        else:
            return getattr(obj, attr, default)

    @post_dump
    def make_obj(self, data, **kwargs):
        if data.get('wager', False) is None:
            del data['wager']
        if data.get('participants', False) is None:
            del data['participants']
        return data


class FetchAllPartySchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    expand = fields.DelimitedList(fields.String(), required=False, missing=[])
    include = fields.DelimitedList(fields.String(), required=False, missing=[])
    name = fields.String(required=False)


class UpdatePartySchema(Schema):
    name = fields.String(required=True)


create_schema = CreatePartySchema()
dump_schema = DumpPartySchema()
dump_many_schema = DumpPartySchema(many=True)
fetch_all_schema = FetchAllPartySchema()
update_schema = UpdatePartySchema()
