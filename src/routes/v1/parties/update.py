from flask import request, g
from flask_restful import marshal_with
from marshmallow import fields, validate, Schema, ValidationError
from .. import Base
from ....common.response import DataResponse
from ....common.auth import check_user
from .... import services


class Update(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    @check_user
    def put(self, uuid):
        json_data = request.get_json()
        try:
            data = UpdateSchema().load(json_data)
        except ValidationError as e:
            self.throw_error(http_code=self.code.BAD_REQUEST, err=e.messages)

        party = services.find_party_by_uuid(uuid=uuid)
        party.name = data['name']
        party = services.save_party(party)
        party_result = services.dump_party(party)
        return DataResponse(data={'parties': party_result})


class UpdateSchema(Schema):
    name = fields.String(required=True)
