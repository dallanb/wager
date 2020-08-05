from marshmallow import fields, validate, Schema


class CreateSchema(Schema):
    name = fields.String(required=True)


create_schema = CreateSchema()
