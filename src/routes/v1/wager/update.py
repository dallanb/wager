from flask import request, g
from flask_restful import marshal_with
from marshmallow import fields, validate, Schema, ValidationError
from .. import Base
from .... import services
from ....common.auth import check_user
from ....common.response import DataResponse
from ....common.utils import get_json, time_now


class Update(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    @check_user
    def put(self, uuid):
        try:
            data = self.body_schema.load(get_json(request.form['data']))
        except ValidationError as e:
            self.throw_error(http_code=self.code.BAD_REQUEST, err=e.messages)

        wager = services.find_wager_by_uuid(uuid=uuid)
        if not wager:
            raise self.throw_error(http_code=self.code.NOT_FOUND)

        if not services.is_owner(wager, g.user):
            raise self.throw_error(http_code=self.code.UNAUTHORIZED,
                                   err={"wager": ["Update is only available to owner"]})

        # time
        if data['time']:
            wager.time = data['time']

        # course
        if data['course']:
            course = services.assign_wager_course_by_uuid(uuid=data['course'])
            wager.course_uuid = course.uuid

        # party
        if data['members']:
            # once a party is set it can no longer be updated
            if wager.party:
                self.throw_error(http_code=self.code.BAD_REQUEST)
            party = services.assign_wager_party_by_members(members=data['members'])
            wager.party_uuid = party.uuid

        # stake
        if data['currency'] or data['amount']:
            stake = services.assign_wager_stake(currency=data['currency'], amount=data['amount'])
            wager.stake_uuid = stake.uuid

        wager = services.save_wager(wager)
        wager_result = services.dump_wager(wager)
        return DataResponse(data={'wager': wager_result})


class UpdateSchema(Schema):
    time = fields.Int(required=False, validate=validate.Range(min=time_now(), min_inclusive=False,
                                                              error="Must be greater than current time"), missing=None)
    currency = fields.Str(required=False, missing=None)
    amount = fields.Str(required=False, missing=None)
    course = fields.UUID(required=False, missing=None)
    members = fields.List(fields.Str(required=True), required=False, missing=None)
