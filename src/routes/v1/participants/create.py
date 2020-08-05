from flask import request
from flask_restful import marshal_with
from marshmallow import ValidationError
from .. import Base
from ....common.response import DataResponse
from ....common.auth import check_user
from ....schemas import create_participant_schema
from .... import services


class Create(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    @check_user
    def post(self, uuid):
        json_data = request.get_json()
        try:
            data = create_participant_schema.load(json_data)
        except ValidationError as e:
            self.throw_error(http_code=self.code.BAD_REQUEST, err=e.messages)

        party = services.find_party_by_uuid(uuid=uuid)
        if not party:
            self.throw_error(http_code=self.code.NOT_FOUND)

        participant = services.init_participant(user_uuid=data['user_uuid'], party_uuid=party.uuid, status="pending")
        participant = services.save_participant(participant=participant)
        participant_result = services.dump_participant(participant)
        return DataResponse(data={'participants': participant_result})
