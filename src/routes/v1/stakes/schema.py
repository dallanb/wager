from marshmallow import fields, validate, Schema
from sqlalchemy_utils import CurrencyType
from ..participants.schema import DumpSchema as DumpParticipantSchema
from ....common.cleaner import is_currency


class CreateSchema(Schema):
    currency = fields.Str(required=True, validate=[lambda currency: is_currency(currency) == currency])
    amount = fields.Number(required=True, validate=validate.Range(min=0, error="Cannot be a negative value."),
                           as_string=True)


class DumpSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    currency = CurrencyType()
    amount = fields.String()
    participant = fields.Nested(DumpParticipantSchema)


class FetchAllSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)


class UpdateSchema(Schema):
    currency = fields.Str(required=False, missing=None, validate=[lambda currency: is_currency(currency) == currency])
    amount = fields.Number(required=False, missing=None,
                           validate=validate.Range(min=0, error="Cannot be a negative value."),
                           as_string=True)


create_schema = CreateSchema()
dump_schema = DumpSchema()
dump_many_schema = DumpSchema(many=True)
fetch_all_schema = FetchAllSchema()
update_schema = UpdateSchema()
