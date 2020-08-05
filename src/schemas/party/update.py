from marshmallow import fields, validate, Schema


class UpdateSchema(Schema):
    name = fields.String(required=True)


update_schema = UpdateSchema()
