from marshmallow import fields, Schema


class FetchAllSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)


fetch_all_schema = FetchAllSchema()
