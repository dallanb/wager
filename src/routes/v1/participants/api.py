from flask import request
from flask_restful import marshal_with
from .schema import *
from ..base import Base
from ....common.response import DataResponse
from ....common.auth import check_user
from ....models import Participant, Party


class ParticipantsAPI(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    def get(self, uuid):
        participants = self.find(model=Participant, uuid=uuid, not_found=self.code.NOT_FOUND)
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

    @marshal_with(DataResponse.marshallable())
    def get(self):
        data = self.clean(schema=fetch_all_schema, instance=request.args)
        participants = self.find(model=Participant, **data)
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
        parties = self.find(model=Party, uuid=uuid, not_found=self.code.NOT_FOUND)
        participant = self.init(model=Participant, user_uuid=data['user_uuid'], party=parties.items[0],
                                status="pending")
        participant = self.save(instance=participant)
        return DataResponse(
            data={
                'participants': self.dump(
                    schema=dump_schema,
                    instance=participant
                )
            }
        )
