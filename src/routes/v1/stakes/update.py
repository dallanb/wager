from flask import request
from flask_restful import marshal_with
from marshmallow import ValidationError
from .. import Base
from ....common.response import DataResponse
from ....common.auth import check_user
from ....schemas import update_stake_schema
from .... import services


class Update(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    @check_user
    def put(self, uuid):
        json_data = request.get_json()
        try:
            data = update_stake_schema.load(json_data)
        except ValidationError as e:
            self.throw_error(http_code=self.code.BAD_REQUEST, err=e.messages)
        stake = services.find_stake_by_uuid(uuid=uuid)
        for k, v in data.items():
            stake.__setattr__(k, v)
        stake = services.save_stake(stake)
        stake_result = services.dump_stake(stake)
        return DataResponse(data={'stakes': stake_result})
