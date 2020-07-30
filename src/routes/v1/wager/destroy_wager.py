from flask_restful import marshal_with
from .. import Base
from ....common import MessageResponse
from ....common.error import *
from .... import services


class DestroyWager(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(MessageResponse.marshallable())
    @Base.check_user
    def delete(self, **kwargs):
        try:
            # retrieve uuid
            uuid = kwargs.get('uuid', None)

            # find wager
            wager = services.find_wager_by_uuid(uuid=uuid)
            if not wager:
                raise InvalidParamError('uuid')

            # destroy wager
            services.destroy_wager(wager)

            return MessageResponse()
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
