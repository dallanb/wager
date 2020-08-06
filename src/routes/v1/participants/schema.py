from marshmallow import Schema, post_dump
from marshmallow_enum import EnumField
from webargs import fields
from ....common import ParticipantStatusEnum
import logging


class CreateParticipantSchema(Schema):
    user_uuid = fields.UUID(required=True)
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    party = fields.Nested('DumpPartySchema')


class DumpParticipantSchema(Schema):
    status = EnumField(ParticipantStatusEnum)
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    user_uuid = fields.UUID()
    party = fields.Nested('DumpPartySchema',
                          include=('uuid', 'ctime', 'mtime', 'name', 'wager'))
    stakes = fields.List(fields.Nested('DumpStakeSchema', exclude=('participant',)))

    def get_attribute(self, obj, attr, default):
        if attr == 'party':
            logging.info(getattr(obj, attr, default))
            return getattr(obj, attr, default) if any(
                attr in expand for expand in self.context.get('expand', [])) else None
        if attr == 'stakes':
            return getattr(obj, attr, default) if any(
                attr in include for include in self.context.get('include', [])) else None
        else:
            return getattr(obj, attr, default)

    @post_dump
    def make_obj(self, data, **kwargs):
        if data.get('party', False) is None:
            del data['party']
        if data.get('stakes', False) is None:
            del data['stakes']
        return data


class FetchAllParticipantSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    expand = fields.DelimitedList(fields.String(), required=False, missing=[])
    include = fields.DelimitedList(fields.String(), required=False, missing=[])
    user_uuid = fields.UUID(required=False)


create_schema = CreateParticipantSchema()
dump_schema = DumpParticipantSchema()
dump_many_schema = DumpParticipantSchema(many=True)
fetch_all_schema = FetchAllParticipantSchema()
