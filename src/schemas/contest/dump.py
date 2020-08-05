from marshmallow import fields, Schema
from src.schemas.wager.dump import DumpSchema as DumpWagerSchema


class DumpSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    wager = fields.Nested(DumpWagerSchema)
    contest_uuid = fields.UUID()


dump_schema = DumpSchema()
dump_many_schema = DumpSchema(many=True)
