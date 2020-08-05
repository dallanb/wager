from marshmallow import fields, Schema


class CreateSchema(Schema):
    contest_uuid = fields.UUID()


create_schema = CreateSchema()
