from marshmallow import Schema
from webargs import fields


class ParticipantActiveSchema(Schema):
    uuid = fields.UUID(attribute='participant.uuid')
    member_uuid = fields.UUID(attribute='participant.member_uuid')
