from marshmallow import validate, Schema, post_dump
from webargs import fields


class CreateStakeSchema(Schema):
    amount = fields.Number(required=True, validate=validate.Range(min=0, error="Cannot be a negative value."),
                           as_string=True)


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


class UpdateStakeSchema(Schema):
    amount = fields.Number(required=False, missing=None,
                           validate=validate.Range(min=0, error="Cannot be a negative value."),
                           as_string=True)


create_schema = CreateStakeSchema()
dump_schema = DumpStakeSchema()
dump_many_schema = DumpStakeSchema(many=True)
update_schema = UpdateStakeSchema()
