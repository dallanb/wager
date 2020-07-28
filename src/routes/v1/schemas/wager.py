from marshmallow import fields, Schema


class CreateWagerSchema(Schema):
    time = fields.Str(required=False)
    currency = fields.Str(required=False)
    amount = fields.Str(required=False)
    course = fields.Str(required=False)
    members = fields.List(fields.Str(required=True), required=False)
