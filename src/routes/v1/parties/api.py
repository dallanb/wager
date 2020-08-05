from flask import request
from flask_restful import marshal_with
from marshmallow import ValidationError
from .schema import *
from ..base import Base
from ....common.response import DataResponse
from ....common.auth import check_user
from .... import services


class PartiesAPI(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    def get(self, uuid):
        party = services.find_party_by_uuid(uuid=uuid)
        if not party:
            self.throw_error(http_code=self.code.NOT_FOUND)
        party_result = services.dump_party(schema=dump_schema, party=party)
        return DataResponse(data={'parties': party_result})

    @marshal_with(DataResponse.marshallable())
    @check_user
    def put(self, uuid):
        json_data = request.get_json()
        try:
            data = services.clean_party(schema=update_schema, party=json_data)
        except ValidationError as e:
            self.throw_error(http_code=self.code.BAD_REQUEST, err=e.messages)

        party = services.find_party_by_uuid(uuid=uuid)
        party.name = data['name']
        party = services.save_party(party)
        party_result = services.dump_party(schema=dump_schema, party=party)
        return DataResponse(data={'parties': party_result})


class PartiesListAPI(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    def get(self):
        try:
            data = services.clean_party(schema=fetch_all_schema, party=request.args)
            self.logger.info(data)
        except ValidationError as e:
            self.throw_error(http_code=self.code.BAD_REQUEST, err=e.messages)
        parties = services.find_party(page=data['page'], per_page=data['per_page'])
        total = services.count_party()
        party_result = services.dump_party(schema=dump_many_schema, party=parties, params={'expand': data['expand']})
        _metadata = self.prepare_metadata(total=total, page=data['page'], per_page=data['per_page'])
        return DataResponse(
            data={'_metadata': _metadata, 'parties': party_result})

    @marshal_with(DataResponse.marshallable())
    @check_user
    def post(self, uuid):
        json_data = request.get_json()
        try:
            data = services.clean_party(schema=create_schema, party=json_data)
        except ValidationError as e:
            self.throw_error(http_code=self.code.BAD_REQUEST, err=e.messages)

        wager = services.find_wager_by_uuid(uuid=uuid)
        if not wager:
            self.throw_error(http_code=self.code.NOT_FOUND)

        party = services.init_party(name=data['name'], wager=wager)
        party = services.save_party(party=party)
        party_result = services.dump_party(schema=dump_schema, party=party)
        return DataResponse(data={'parties': party_result})
