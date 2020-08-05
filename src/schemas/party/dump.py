from marshmallow import fields, validate, Schema
from src.schemas.wager.dump import DumpSchema as DumpWagerSchema


class DumpSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    name = fields.String()
    wager = fields.Nested(DumpWagerSchema)


dump_schema = DumpSchema()
dump_many_schema = DumpSchema(many=True)
