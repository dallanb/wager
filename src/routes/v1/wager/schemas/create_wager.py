from marshmallow import fields, Schema


class CreateWagerSchema(Schema):
    time = fields.Int(required=False)
    currency = fields.Str(required=False)
    amount = fields.Str(required=False)
    course = fields.UUID(required=False)
    members = fields.List(fields.Str(required=True), required=False)
