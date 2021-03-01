from marshmallow import Schema, pre_dump
from webargs import fields


class ParticipantActiveSchema(Schema):
    uuid = fields.UUID(attribute='participant.uuid')
    member_uuid = fields.UUID(attribute='participant.member_uuid')
    stake = fields.Float(attribute='stake.amount')

    @pre_dump
    def prepare(self, data, **kwargs):
        data['stake'] = data['participant'].stake
        return data
