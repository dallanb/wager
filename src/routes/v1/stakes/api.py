from flask import request
from flask_restful import marshal_with
from marshmallow import ValidationError
from .schema import *
from ..base import Base
from ....common.response import DataResponse, MessageResponse
from ....common.auth import check_user
from .... import services


class StakesAPI(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    @check_user
    def put(self, uuid):
        json_data = request.get_json()
        try:
            data = services.clean_stake(schema=update_schema, stake=json_data)
        except ValidationError as e:
            self.throw_error(http_code=self.code.BAD_REQUEST, err=e.messages)

        stakes = services.find_stakes(uuid=uuid)
        if not stakes.total:
            self.throw_error(http_code=self.code.NOT_FOUND)

        stake = stakes.items[0]
        for k, v in data.items():
            stake.__setattr__(k, v)
        stake = services.save_stake(stake)
        stake_result = services.dump_stake(schema=dump_schema, stake=stake)
        return DataResponse(data={'stakes': stake_result})

    @marshal_with(MessageResponse.marshallable())
    def delete(self, uuid):
        stakes = services.find_stakes(uuid=uuid)
        if not stakes.total:
            self.throw_error(http_code=self.code.NOT_FOUND)

        services.destroy_stake(stakes.items[0])
        return MessageResponse()


class StakesListAPI(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    @check_user
    def post(self, uuid):
        json_data = request.get_json()
        try:
            data = services.clean_stake(schema=create_schema, stake=json_data)
        except ValidationError as e:
            self.throw_error(http_code=self.code.BAD_REQUEST, err=e.messages)

        participants = services.find_participants(uuid=uuid)
        if not participants.total:
            self.throw_error(http_code=self.code.NOT_FOUND)

        stake = services.init_stake(currency=data['currency'], amount=data['amount'], participant=participants.items[0])
        stake = services.save_stake(stake=stake)
        stake_result = services.dump_stake(schema=dump_schema, stake=stake)
        return DataResponse(data={'stakes': stake_result})
