from flask import request
from flask_restful import marshal_with
from marshmallow import ValidationError
from .schema import *
from ..base import Base
from ....common.response import DataResponse
from ....common.auth import check_user
from .... import services


class ParticipantsAPI(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    def get(self, uuid):
        participant = services.find_participant(uuid=uuid, single=True)
        if not participant:
            self.throw_error(http_code=self.code.NOT_FOUND)
        participant_result = services.dump_participant(schema=dump_schema, participant=participant)
        return DataResponse(data={'participants': participant_result})


class ParticipantsListAPI(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    def get(self):
        try:
            data = services.clean_participant(schema=fetch_all_schema, participant=request.args)
            self.logger.info(data)
        except ValidationError as e:
            self.throw_error(http_code=self.code.BAD_REQUEST, err=e.messages)
        participants = services.find_participant(**data)
        self.logger.info(participants)
        total = services.count_participant()
        participant_result = services.dump_participant(schema=dump_many_schema, participant=participants,
                                                       params={'expand': data['expand']})
        _metadata = self.prepare_metadata(total=total, page=data['page'], per_page=data['per_page'])
        return DataResponse(
            data={'_metadata': _metadata, 'participants': participant_result})

    @marshal_with(DataResponse.marshallable())
    @check_user
    def post(self, uuid):
        json_data = request.get_json()
        try:
            data = services.clean_participant(schema=create_schema, participant=json_data)
        except ValidationError as e:
            self.throw_error(http_code=self.code.BAD_REQUEST, err=e.messages)

        party = services.find_party_by_uuid(uuid=uuid)
        if not party:
            self.throw_error(http_code=self.code.NOT_FOUND)

        participant = services.init_participant(user_uuid=data['user_uuid'], party_uuid=party.uuid, status="pending")
        participant = services.save_participant(participant=participant)
        participant_result = services.dump_participant(schema=dump_schema, participant=participant)
        return DataResponse(data={'participants': participant_result})
