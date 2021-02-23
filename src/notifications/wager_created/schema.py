from marshmallow import Schema
from webargs import fields


class WagerCreatedSchema(Schema):
    uuid = fields.UUID(attribute='wager.uuid')
