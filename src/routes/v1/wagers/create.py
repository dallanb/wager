from flask import request, g
from flask_restful import marshal_with
from marshmallow import fields, validate, Schema, ValidationError
from .. import Base
from ....common.response import DataResponse
from ....common.auth import check_user
from .... import services


class Create(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    @check_user
    def post(self):
        json_data = request.get_json()
        try:
            data = CreateSchema().load(json_data)
        except ValidationError as e:
            self.throw_error(http_code=self.code.BAD_REQUEST, err=e.messages)

        wager = services.init_wager(status='pending', owner_uuid=g.user)
        services.init_contest(contest_uuid=data['contest_uuid'], wager=wager)
        wager = services.save_wager(wager)
        wager_result = services.dump_wager(wager)
        return DataResponse(data={'wagers': wager_result})


class CreateSchema(Schema):
    contest_uuid = fields.UUID(required=True)
