from flask import request
from flask_restful import marshal_with
from .schemas import CreateWagerSchema
from .. import Base
from ....services import Wager as WagerService
from ....common import DataResponse, get_json


class CreateWager(Base):
    def __init__(self):
        Base.__init__(self)
        self.service = WagerService()
        self.schema = CreateWagerSchema()

    @marshal_with(DataResponse.marshallable())
    @Base.check_user
    def post(self):
        try:
            # clean payload
            data = self.schema.load(get_json(request.form['data']))
            # create wager
            wager = self.service.create_wager()
            # assign wager attrs
            wager.course = self.service.assign_course(course=data.get('course'))
            wager.owner = self.service.assign_owner()
            wager.party = self.service.assign_party(members=data.get('members'))
            wager.stake = self.service.assign_stake(currency=data.get('currency'), amount=data.get('amount'))
            wager.status = self.service.assign_status()
            wager.time = self.service.assign_time(time=data.get('time'))
            # save wager
            wager = self.service.save_wager(wager)
            # dump wager
            wager_result = self.service.dump_wager(wager)
            return DataResponse(data={'wager': wager_result})
        except ValueError as e:
            self.error.info(e)
            self.throw_error(http_code=self.code.BAD_REQUEST, msg=e)
        except Exception as e:
            self.error.info(e)
            self.throw_error(self.code.INTERNAL_SERVER_ERROR)
