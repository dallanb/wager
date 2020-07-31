from flask_restful import marshal_with
from .. import Base
from .... import services
from ....common import DataResponse


class Fetch(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    def get(self, uuid):
        wager = services.find_wager_by_uuid(uuid=uuid)
        if not wager:
            self.throw_error(http_code=self.code.NOT_FOUND)
        wager_result = services.dump_wager(wager)
        return DataResponse(data={'wager': wager_result})
