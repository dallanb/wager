from flask import request, g
from flask_restful import marshal_with
from .schemas import CreateWagerSchema
from .. import Base
from ....common import DataResponse, get_json
from ....common.error import *
from .... import services


class CreateWager(Base):
    def __init__(self):
        Base.__init__(self)
        self.schema = CreateWagerSchema()

    @marshal_with(DataResponse.marshallable())
    @Base.check_user
    def post(self):
        try:
            # clean payload
            data = self.schema.load(get_json(request.form['data']))

            # create wager
            wager = services.init_wager()

            # set owner
            wager.owner = g.user

            # set status
            status = services.find_wager_status_by_enum(status_enum='active')
            wager.status_uuid = status.uuid

            # set time
            if data.get('time'):
                wager.time = data.get('time')

            # set course
            if data.get('course'):
                course = services.assign_wager_course_by_uuid(uuid=data.get('course'))
                wager.course_uuid = course.uuid

            # set party
            if data.get('members'):
                party = services.assign_wager_party_by_members(members=data.get('members'))
                wager.party_uuid = party.uuid

            # set stake
            if data.get('currency') or data.get('amount'):
                stake = services.assign_wager_stake(currency=data.get('currency'), amount=data.get('amount'))
                wager.stake_uuid = stake.uuid

            # save wager
            wager = services.save_wager(wager)

            # dump wager
            wager_result = services.dump_wager(wager)

            return DataResponse(data={'wager': wager_result})
        except InvalidParamError as e:
            self.logger.error(e)
            self.throw_error(http_code=self.code.BAD_REQUEST, msg=e)
        except InvalidTypeError as e:
            self.logger.error(e)
            self.throw_error(http_code=self.code.BAD_REQUEST, msg=e)
        except MissingParamError as e:
            self.logger.error(e)
            self.throw_error(http_code=self.code.BAD_REQUEST, msg=e)
        except Exception as e:
            self.logger.error(e)
            self.throw_error(self.code.INTERNAL_SERVER_ERROR)
