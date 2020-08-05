from marshmallow import fields, validate, Schema
from ...common.cleaner import is_currency


class CreateSchema(Schema):
    currency = fields.Str(required=True, validate=[lambda currency: is_currency(currency) == currency])
    amount = fields.Number(required=True, validate=validate.Range(min=0, error="Cannot be a negative value."),
                           as_string=True)


create_schema = CreateSchema()
