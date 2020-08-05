from marshmallow import fields, Schema


class CreateSchema(Schema):
    user_uuid = fields.UUID(required=True)


create_schema = CreateSchema()
