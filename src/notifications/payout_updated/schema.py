from marshmallow import Schema, pre_dump
from webargs import fields


class PayoutUpdatedSchema(Schema):
    uuid = fields.UUID(attribute='wager.uuid')
    contest_uuid = fields.UUID(attribute='contest.contest_uuid')

    @pre_dump
    def prepare(self, data, **kwargs):
        wager = data['wager']
        data['contest'] = wager.contest
        return data
