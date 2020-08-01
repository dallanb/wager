from flask import request, g
from flask_restful import marshal_with
from marshmallow import fields, validate, Schema, ValidationError
from .. import Base
from .... import services
from ....common.auth import check_user
from ....common.response import DataResponse
from ....common.utils import add_years, time_now
from ....common.cleaner import is_currency


class Update(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    @check_user
    def put(self, uuid):
        json_data = request.get_json()
        if not json_data:
            self.throw_error(http_code=self.code.BAD_REQUEST)
        try:
            data = UpdateSchema().load(json_data)
        except ValidationError as e:
            self.throw_error(http_code=self.code.BAD_REQUEST, err=e.messages)

        wager = services.find_wager_by_uuid(uuid=uuid)
        if not wager:
            raise self.throw_error(http_code=self.code.NOT_FOUND)

        if not services.is_owner(wager, g.user):
            raise self.throw_error(http_code=self.code.FORBIDDEN,
                                   err={"wager": ["Update is only available to owner"]})

        # time
        if data['time']:
            wager.time = data['time']

        # course
        if data['course']:
            course = services.find_course_by_uuid(uuid=data['course'])
            if not course:
                self.throw_error(http_code=self.code.BAD_REQUEST, err={'course': ['Invalid UUID.']})
            wager.course_uuid = course.uuid

        # party
        if data['opponents']:
            # once a party is set it can no longer be updated
            if wager.party_uuid:
                self.throw_error(http_code=self.code.BAD_REQUEST)
            party = services.assign_wager_party_by_members(members=[*data['opponents'], wager.owner])
            wager.party_uuid = party.uuid

        # stake
        if data['currency'] or data['amount']:
            stake = services.assign_wager_stake(currency=data['currency'], amount=data['amount'])
            wager.stake_uuid = stake.uuid

        wager = services.save_wager(wager)
        wager_result = services.dump_wager(wager)
        return DataResponse(data={'wager': wager_result})


class UpdateSchema(Schema):
    time = fields.Int(required=False, validate=[validate.Range(min=time_now(), min_inclusive=False,
                                                               error="Must be greater than current time."),
                                                validate.Range(max=add_years(time_now(), 1),
                                                               error="Must be within the next year.")], missing=None)
    currency = fields.Str(required=False, missing=None, validate=[lambda currency: is_currency(currency) == currency])
    amount = fields.Number(required=False, validate=validate.Range(min=0, error="Cannot be a negative value."),
                           missing=None, as_string=True)
    course = fields.UUID(required=False, missing=None)
    opponents = fields.List(fields.UUID(required=True),
                            validate=[validate.Length(equal=1),
                                      lambda opponents: len(set(opponents)) != len({*opponents, g.user}),
                                      lambda opponents: len(opponents) == len(set(opponents))],
                            required=False, missing=None)
