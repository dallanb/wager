from marshmallow import validate, Schema, post_dump
from webargs import fields
from sqlalchemy_utils import CurrencyType
from ....common.cleaner import is_currency
import logging


class CreateStakeSchema(Schema):
    currency = fields.Str(required=True, validate=[lambda currency: is_currency(currency) == currency])
    amount = fields.Number(required=True, validate=validate.Range(min=0, error="Cannot be a negative value."),
                           as_string=True)


class DumpStakeSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    currency = CurrencyType()
    amount = fields.String()
    participant = fields.Nested('DumpParticipantSchema', only=("uuid", "ctime", "mtime", "status", "user_uuid"))

    def get_attribute(self, obj, attr, default):
        if attr == 'participant':
            logging.info(self.context.get('expand', []))
            logging.info(getattr(obj, attr, default) if any(
                attr in expand for expand in self.context.get('expand', [])) else None)
            return getattr(obj, attr, default) if any(
                attr in expand for expand in self.context.get('expand', [])) else None
        else:
            return getattr(obj, attr, default)

    @post_dump
    def make_obj(self, data, **kwargs):
        if data.get('participant', False) is None:
            del data['participant']
        return data


class FetchAllStakeSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    expand = fields.DelimitedList(fields.String(), required=False, missing=[])


class UpdateStakeSchema(Schema):
    currency = fields.Str(required=False, missing=None, validate=[lambda currency: is_currency(currency) == currency])
    amount = fields.Number(required=False, missing=None,
                           validate=validate.Range(min=0, error="Cannot be a negative value."),
                           as_string=True)


create_schema = CreateStakeSchema()
dump_schema = DumpStakeSchema()
dump_many_schema = DumpStakeSchema(many=True)
fetch_all_schema = FetchAllStakeSchema()
update_schema = UpdateStakeSchema()
