from flask_restful import marshal_with
from .. import Base
from .... import services
from ....common import DataResponse


class Fetch(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    def get(self, uuid):
        stake = services.find_stake_by_uuid(uuid=uuid)
        if not stake:
            self.throw_error(http_code=self.code.NOT_FOUND)
        stake_result = services.dump_stake(stake=stake)
        return DataResponse(data={'stakes': stake_result})
