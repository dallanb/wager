from flask_restful import marshal_with
from .. import Base
from ....common.response import MessageResponse
from ....common.auth import check_user
from .... import services


class Destroy(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(MessageResponse.marshallable())
    @check_user
    def delete(self, uuid):
        wager = services.find_wager_by_uuid(uuid=uuid)
        if not wager:
            self.throw_error(http_code=self.code.NOT_FOUND)
        services.destroy_wager(wager)
        return MessageResponse()
