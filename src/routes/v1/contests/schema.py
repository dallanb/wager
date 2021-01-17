from marshmallow import fields, Schema


class DumpContestSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    wager = fields.Nested('DumpWagerSchema')
    contest_uuid = fields.UUID()


class DumpContestCompleteSchema(Schema):
    uuid = fields.UUID()
    parties = fields.Integer()
    total_payout = fields.Float()
    buy_in = fields.Float()
    party_payouts = fields.List(fields.Dict(keys=fields.Integer(), values=fields.Float()))


dump_schema = DumpContestSchema()
dump_many_schema = DumpContestSchema(many=True)
dump_complete_schema = DumpContestCompleteSchema()
