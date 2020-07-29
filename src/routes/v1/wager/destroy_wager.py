from flask_restful import marshal_with
from .. import Base
from ....services import Wager as WagerService
from ....common import MessageResponse


class DestroyWager(Base):
    def __init__(self):
        Base.__init__(self)
        self.service = WagerService()

    @marshal_with(MessageResponse.marshallable())
    @Base.check_user
    def delete(self, **kwargs):
        # retrieve uuid
        uuid = kwargs.get('uuid', None)
        # destroy wager
        wager = self.service.destory_wager(uuid=uuid)
        return MessageResponse()
