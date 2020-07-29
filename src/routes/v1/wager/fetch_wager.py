from flask_restful import marshal_with
from .. import Base
from ....services import Wager as WagerService
from ....common import DataResponse


class FetchWager(Base):
    def __init__(self):
        Base.__init__(self)
        self.service = WagerService()

    @marshal_with(DataResponse.marshallable())
    def get(self, **kwargs):
        # retrieve uuid
        uuid = kwargs.get('uuid', None)
        # find wager
        wagers = self.service.find_wager(uuid=uuid)
        # dump wager
        wagers_result = self.service.dump_wager(wagers, many=True)

        return DataResponse(data={'wager': wagers_result})
