# from flask import request
from flask_restful import marshal_with, request
from .schemas import FetchAllWagerSchema
from .. import Base
from .... import services
from ....common import DataResponse
from ....common.error import *


class FetchAllWager(Base):
    def __init__(self):
        Base.__init__(self)
        self.schema = FetchAllWagerSchema()

    @marshal_with(DataResponse.marshallable())
    def get(self):
        try:
            # clean payload
            data = self.schema.load(request.args)
            page = data.get('page', None)
            per_page = data.get('per_page', None)

            # find wager
            wager = services.find_wager(page=page, per_page=per_page)

            # get wager count
            count = services.count_wager()

            # dump wager
            wager_result = services.dump_wager(wager, many=True)

            return DataResponse(
                data={'_metadata': {'total': count, 'page': page, 'per_page': per_page}, 'wager': wager_result})
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
