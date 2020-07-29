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
        # clean payload
        data = self.schema.load(get_json(request.form['data']))
        # create wager
        wager = self.service.create_wager(**data)
        # dump wager
        wager_result = self.service.dump_wager(wager)

        return DataResponse(data={'wager': wager_result})
