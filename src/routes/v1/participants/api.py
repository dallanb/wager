from uuid import uuid4

from flask import request
from flask_restful import marshal_with

from .schema import *
from ..base import Base
from ....common.response import DataResponse
from ....services import ParticipantService, PartyService


class ParticipantsAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.participant = ParticipantService()

    @marshal_with(DataResponse.marshallable())
    def get(self, uuid):
        participants = self.participant.find(uuid=uuid)
        if not participants.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        return DataResponse(
            data={
                'participants': self.dump(
                    schema=dump_schema,
                    instance=participants.items[0]
                )
            }
        )

    @marshal_with(DataResponse.marshallable())
    def put(self, uuid):
        participant = self.participant.update(uuid=uuid, member_uuid=uuid4())
        # if not participants.total:
        #     self.throw_error(http_code=self.code.NOT_FOUND)
        return DataResponse(
            data={
                'participants': self.dump(
                    schema=dump_schema,
                    instance=participant
                )
            }
        )


class ParticipantsListAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.participant = ParticipantService()
        self.party = PartyService()

    @marshal_with(DataResponse.marshallable())
    def get(self):
        data = self.clean(schema=fetch_all_schema, instance=request.args)
        participants = self.participant.find(**data)
        return DataResponse(
            data={
                '_metadata': self.prepare_metadata(
                    total_count=participants.total,
                    page_count=len(participants.items),
                    page=data['page'],
                    per_page=data['per_page']
                ),
                'participants': self.dump(
                    schema=dump_many_schema,
                    instance=participants.items,
                    params={
                        'expand': data['expand'],
                        'include': data['include']
                    }
                )
            }
        )
