from marshmallow import fields, Schema

class DumpContestSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    wager = fields.Nested('DumpWagerSchema')
    contest_uuid = fields.UUID()


dump_schema = DumpContestSchema()
dump_many_schema = DumpContestSchema(many=True)