from flask import request
from flask_restful import marshal_with
from marshmallow import ValidationError
from .. import Base
from ....common.response import DataResponse
from ....common.auth import check_user
from ....schemas import create_party_schema
from .... import services


class Create(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    @check_user
    def post(self, uuid):
        json_data = request.get_json()
        try:
            data = create_party_schema.load(json_data)
        except ValidationError as e:
            self.throw_error(http_code=self.code.BAD_REQUEST, err=e.messages)

        wager = services.find_wager_by_uuid(uuid=uuid)
        if not wager:
            self.throw_error(http_code=self.code.NOT_FOUND)

        party = services.init_party(name=data['name'], wager=wager)
        party = services.save_party(party=party)
        party_result = services.dump_party(party)
        return DataResponse(data={'parties': party_result})
