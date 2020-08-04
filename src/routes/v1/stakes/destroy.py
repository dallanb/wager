from flask_restful import marshal_with
from .. import Base
from .... import services
from ....common import MessageResponse


class Destroy(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(MessageResponse.marshallable())
    def delete(self, uuid):
        stake = services.find_stake_by_uuid(uuid=uuid)
        if not stake:
            self.throw_error(http_code=self.code.NOT_FOUND)
        services.destroy_stake(stake)
        return MessageResponse()
