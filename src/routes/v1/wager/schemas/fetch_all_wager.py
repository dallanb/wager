from marshmallow import fields, Schema


class FetchAllWagerSchema(Schema):
    page = fields.Int(required=False)
    per_page = fields.Int(required=False)
