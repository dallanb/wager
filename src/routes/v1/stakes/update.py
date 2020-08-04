from flask import request
from flask_restful import marshal_with
from marshmallow import fields, validate, Schema, ValidationError
from .. import Base
from ....common.response import DataResponse
from ....common.auth import check_user
from ....common.cleaner import is_currency
from .... import services


class Update(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    @check_user
    def put(self, uuid):
        json_data = request.get_json()
        try:
            data = UpdateSchema().load(json_data)
        except ValidationError as e:
            self.throw_error(http_code=self.code.BAD_REQUEST, err=e.messages)
        self.logger.info(data)
        stake = services.find_stake_by_uuid(uuid=uuid)
        for k, v in data.items():
            stake.__setattr__(k, v)
        stake = services.save_stake(stake)
        stake_result = services.dump_stake(stake)
        return DataResponse(data={'stakes': stake_result})


class UpdateSchema(Schema):
    currency = fields.Str(required=False, missing=None, validate=[lambda currency: is_currency(currency) == currency])
    amount = fields.Number(required=False, missing=None,
                           validate=validate.Range(min=0, error="Cannot be a negative value."),
                           as_string=True)
