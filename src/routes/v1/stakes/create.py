from flask import request
from flask_restful import marshal_with
from marshmallow import ValidationError
from .. import Base
from ....common.response import DataResponse
from ....common.auth import check_user
from ....schemas import create_stake_schema
from .... import services


class Create(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    @check_user
    def post(self, uuid):
        json_data = request.get_json()
        try:
            data = create_stake_schema.load(json_data)
        except ValidationError as e:
            self.throw_error(http_code=self.code.BAD_REQUEST, err=e.messages)

        participant = services.find_participant_by_uuid(uuid=uuid)
        if not participant:
            self.throw_error(http_code=self.code.NOT_FOUND)

        stake = services.init_stake(currency=data['currency'], amount=data['amount'], participant_uuid=participant.uuid)
        stake = services.save_stake(stake=stake)
        stake_result = services.dump_stake(stake)
        return DataResponse(data={'stakes': stake_result})
