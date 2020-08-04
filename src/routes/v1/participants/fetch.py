from flask_restful import marshal_with
from .. import Base
from .... import services
from ....common import DataResponse


class Fetch(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    def get(self, uuid):
        participant = services.find_participant_by_uuid(uuid=uuid)
        if not participant:
            self.throw_error(http_code=self.code.NOT_FOUND)
        participant_result = services.dump_participant(participant=participant)
        return DataResponse(data={'participants': participant_result})
