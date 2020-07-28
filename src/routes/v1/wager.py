from flask_restful import marshal_with
from . import Base
from ...models import WagerModel, WagerSchema
from ...common import DataResponse, MessageResponse


class Wager(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    def get(self, uuid=None):
        filter = [] if uuid is None else [WagerModel.uuid == uuid]
        wagers = WagerModel.query.filter(*filter).all()
        self.logger.info(wagers)
        wagers_result = [] if not wagers else wagersWagerSchema.dump(wagers)
        self.logger.info(wagers_result)
        return DataResponse(data={'wagers': wagers_result})

    @marshal_with(DataResponse.marshallable())
    def post(self):
        return DataResponse(data=False)


    @marshal_with(DataResponse.marshallable())
    def put(self, uuid=None):
        return DataResponse(data=False)

    @marshal_with(MessageResponse.marshallable())
    def delete(self, uuid=None):
        return MessageResponse()