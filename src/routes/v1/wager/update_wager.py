from flask import request
from flask_restful import marshal_with
from .schemas import UpdateWagerSchema
from .. import Base
from ....services import Wager as WagerService
from ....common import DataResponse, get_json


class UpdateWager(Base):
    def __init__(self):
        Base.__init__(self)
        self.service = WagerService()
        self.schema = UpdateWagerSchema()

    @marshal_with(DataResponse.marshallable())
    @Base.check_user
    def put(self, **kwargs):
        # retrieve uuid
        uuid = kwargs.get('uuid', None)
        # clean payload
        data = self.schema.load(get_json(request.form['data']))
        # update wager
        wager = self.service.update_wager(uuid=uuid, **data)
        # dump wager
        wager_result = self.service.dump_wager(wager)

        return DataResponse(data={'wager': wager_result})
