from flask_restful import marshal_with
from .. import Base
from .... import services
from ....common import DataResponse


class Fetch(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    def get(self, uuid):
        party = services.find_party_by_uuid(uuid=uuid)
        if not party:
            self.throw_error(http_code=self.code.NOT_FOUND)
        party_result = services.dump_party(party=party)
        return DataResponse(data={'parties': party_result})
