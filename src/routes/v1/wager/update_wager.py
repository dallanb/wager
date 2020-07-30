from flask import request
from flask_restful import marshal_with
from .schemas import UpdateWagerSchema
from .. import Base
from .... import services
from ....common import DataResponse, get_json
from ....common.error import *


class UpdateWager(Base):
    def __init__(self):
        Base.__init__(self)
        self.schema = UpdateWagerSchema()

    @marshal_with(DataResponse.marshallable())
    @Base.check_user
    def put(self, **kwargs):
        try:
            # retrieve uuid
            uuid = kwargs.get('uuid', None)

            # clean payload
            data = self.schema.load(get_json(request.form['data']))

            # find wager
            wager = services.find_wager_by_uuid(uuid=uuid)
            if not wager:
                raise InvalidParamError('uuid')

            # set time
            if data.get('time'):
                wager.time = data.get('time')

            # set course
            if data.get('course'):
                course = services.assign_wager_course_by_uuid(uuid=data.get('course'))
                wager.course_uuid = course.uuid

            # set party
            if data.get('members'):
                # once a party is set it can no longer be updated
                if wager.party:
                    raise InvalidParamError('members')
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
