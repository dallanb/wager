from flask import request
from flask_restful import marshal_with
from . import Base
from .schemas import CreateWagerSchema
from ...models import WagerModel, WagerSchema, WagerPartyModel, WagerPartyMemberModel
from ...services import Wager as WagerService
from ...common import DataResponse, MessageResponse, WagerStatusEnum, get_json


class Wager(Base):
    def __init__(self):
        Base.__init__(self)
        self.service = WagerService(cache=self.cache, db=self.db, logger=self.logger, user=self.user)

    @marshal_with(DataResponse.marshallable())
    def get(self, uuid=None):
        filters = [] if uuid is None else [WagerModel.uuid == uuid]
        wagers = WagerModel.query.filter(*filters).all()
        wagers_result = WagerSchema().dump(wagers, many=True)
        return DataResponse(data={'wagers': wagers_result})

    @marshal_with(DataResponse.marshallable())
    def post(self):
        # get cleaned request payload
        data = CreateWagerSchema().load(get_json(request.form['data']))
        # create wager
        wager = self.service.create_wager()
        # dump wager
        wager_result = self.service.dump_wager(wager)

        return DataResponse(data={'wager': wager_result})

    @marshal_with(DataResponse.marshallable())
    def put(self, uuid=None):
        return DataResponse(data=False)

    @marshal_with(MessageResponse.marshallable())
    def delete(self, uuid=None):
        return MessageResponse()
