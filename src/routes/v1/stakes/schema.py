from marshmallow import validate, Schema, post_dump
from webargs import fields


class DumpStakeSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    amount = fields.String()
    participant = fields.Nested('DumpParticipantSchema', only=("uuid", "ctime", "mtime", "status", "member_uuid"))

    def get_attribute(self, obj, attr, default):
        if attr == 'participant':
            return getattr(obj, attr, default) if any(
                attr in expand for expand in self.context.get('expand', [])) else None
        else:
            return getattr(obj, attr, default)

    @post_dump
    def make_obj(self, data, **kwargs):
        if data.get('participant', False) is None:
            del data['participant']
        return data


dump_schema = DumpStakeSchema()
dump_many_schema = DumpStakeSchema(many=True)
