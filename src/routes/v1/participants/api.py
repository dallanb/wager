from flask import request
from flask_restful import marshal_with
from .schema import *
from ..base import Base
from ....common.response import DataResponse
from ....common.auth import check_user
from ....services import Participant, Party


class ParticipantsAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.participant = Participant()

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


class ParticipantsListAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.participant = Participant()
        self.party = Party()

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

    @marshal_with(DataResponse.marshallable())
    @check_user
    def post(self, uuid):
        data = self.clean(schema=create_schema, instance=request.get_json())
        parties = self.party.find(uuid=uuid)
        if not parties.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        participant = self.participant.create(user_uuid=data['user_uuid'], party=parties.items[0],
                                              status="pending")
        return DataResponse(
            data={
                'participants': self.dump(
                    schema=dump_schema,
                    instance=participant
                )
            }
        )
