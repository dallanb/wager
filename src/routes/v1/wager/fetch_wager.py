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
        try:
            # retrieve uuid
            uuid = kwargs.get('uuid', None)
            # find wager
            wagers = self.service.find_wager(uuid=uuid)
            # dump wager
            wagers_result = self.service.dump_wager(wagers, many=True)
            return DataResponse(data={'wager': wagers_result})
        except ValueError as e:
            self.logger.error(e)
            self.throw_error(http_code=self.code.BAD_REQUEST, msg=e)
        except Exception as e:
            self.logger.error(e)
            self.throw_error(self.code.INTERNAL_SERVER_ERROR)
