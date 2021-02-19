from marshmallow import Schema, pre_dump
from webargs import fields


class StakeCreatedSchema(Schema):
    uuid = fields.UUID(attribute='stake.uuid')
    member_uuid = fields.UUID(attribute='participant.member_uuid')
    amount = fields.Int(attribute='stake.amount')

    @pre_dump
    def prepare(self, data, **kwargs):
        data['participant'] = data['stake'].participant
        return data
