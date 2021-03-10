from marshmallow import Schema, pre_dump
from webargs import fields

from src import services
from src.common import ManualException


class PayoutUpdatedSchema(Schema):
    uuid = fields.UUID(attribute='wager.uuid')
    contest_uuid = fields.UUID(attribute='contest.contest_uuid')

    @pre_dump
    def prepare(self, data, **kwargs):
        wager = data['wager']
        contests = services.ContestService().find(wager_uuid=wager.uuid)
        if contests.total != 1:
            raise ManualException(err=f"issue with contest associated with wager uuid: {str(wager.uuid)}")
        data['contest'] = contests.items[0]
        return data
