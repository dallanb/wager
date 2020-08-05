from marshmallow import fields, validate, Schema
from ...common import is_currency


class UpdateSchema(Schema):
    currency = fields.Str(required=False, missing=None, validate=[lambda currency: is_currency(currency) == currency])
    amount = fields.Number(required=False, missing=None,
                           validate=validate.Range(min=0, error="Cannot be a negative value."),
                           as_string=True)


update_schema = UpdateSchema()
