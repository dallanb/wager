from flask import request, g
from flask_restful import marshal_with
from marshmallow import fields, validate, Schema, ValidationError
from .. import Base
from ....common.response import DataResponse
from ....common.utils import time_now, get_json
from ....common.auth import check_user
from .... import services


class Create(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    @check_user
    def post(self):
        try:
            json_data = get_json(request.form['data'])
            data = CreateSchema().load(json_data)
        except ValidationError as e:
            self.throw_error(http_code=self.code.BAD_REQUEST, err=e.messages)

        wager = services.init_wager()

        # owner
        wager.owner = g.user

        # status
        status = services.find_wager_status_by_enum(status_enum='active')
        wager.status_uuid = status.uuid

        # time
        if data['time']:
            wager.time = data['time']

        # course
        if data['course']:
            course = services.assign_wager_course_by_uuid(uuid=data['course'])
            wager.course_uuid = course.uuid

        # party
        if data['members']:
            party = services.assign_wager_party_by_members(members=data['members'])
            wager.party_uuid = party.uuid

        # stake
        if data['currency'] or data['amount']:
            stake = services.assign_wager_stake(currency=data['currency'], amount=data['amount'])
            wager.stake_uuid = stake.uuid

        wager = services.save_wager(wager)
        wager_result = services.dump_wager(wager)
        return DataResponse(data={'wager': wager_result})


class CreateSchema(Schema):
    time = fields.Int(required=False, validate=validate.Range(min=time_now(), min_inclusive=False,
                                                              error="Must be greater than current time"), missing=None)
    currency = fields.Str(required=False, missing=None)
    amount = fields.Str(required=False, missing=None)
    course = fields.UUID(required=False, missing=None)
    members = fields.List(fields.Str(required=True), required=False, missing=None)
