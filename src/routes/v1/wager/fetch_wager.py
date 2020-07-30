from flask_restful import marshal_with
from .. import Base
from .... import services
from ....common import DataResponse
from ....common.error import *


class FetchWager(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    def get(self, **kwargs):
        try:
            # retrieve uuid
            uuid = kwargs.get('uuid', None)

            # find wager
            wager = services.find_wager_by_uuid(uuid=uuid)

            # dump wager
            wager_result = services.dump_wager(wager)

            return DataResponse(data={'wager': wager_result})
        except InvalidParamError as e:
            self.logger.error(e)
            self.throw_error(http_code=self.code.BAD_REQUEST, msg=e)
        except InvalidTypeError as e:
            self.logger.error(e)
            self.throw_error(http_code=self.code.BAD_REQUEST, msg=e)
        except MissingParamError as e:
            self.logger.error(e)
            self.throw_error(http_code=self.code.BAD_REQUEST, msg=e)
        except Exception as e:
            self.logger.error(e)
            self.throw_error(self.code.INTERNAL_SERVER_ERROR)
