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
        parties = services.find_parties(uuid=uuid)
        if not parties.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        return DataResponse(
            data={
                'parties': services.dump_party(
                    schema=dump_schema,
                    party=parties.items[0]
                )
            }
        )

    @marshal_with(DataResponse.marshallable())
    @check_user
    def put(self, uuid):
        json_data = request.get_json()
        try:
            data = services.clean_party(schema=update_schema, party=json_data)
        except ValidationError as e:
            self.throw_error(http_code=self.code.BAD_REQUEST, err=e.messages)

        parties = services.find_parties(uuid=uuid)
        if not parties.total:
            self.throw_error(http_code=self.code.NOT_FOUND)

        party = parties.items[0]
        for k, v in data.items():
            party.__setattr__(k, v)
        party = services.save_party(party)
        return DataResponse(
            data={
                'parties': services.dump_party(
                    schema=dump_schema,
                    party=party
                )
            }
        )


class PartiesListAPI(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    def get(self):
        try:
            data = services.clean_party(schema=fetch_all_schema, party=request.args)
        except ValidationError as e:
            self.throw_error(http_code=self.code.BAD_REQUEST, err=e.messages)
        parties = services.find_parties(**data)
        return DataResponse(
            data={
                '_metadata': self.prepare_metadata(
                    total_count=parties.total,
                    page_count=len(parties.items),
                    page=data['page'],
                    per_page=data['per_page']
                ),
                'parties': services.dump_party(
                    schema=dump_many_schema,
                    party=parties.items,
                    params={
                        'expand': data['expand'],
                        'include': data['include']
                    }
                )
            }
        )

    @marshal_with(DataResponse.marshallable())
    @check_user
    def post(self, uuid):
        json_data = request.get_json()
        try:
            data = services.clean_party(schema=create_schema, party=json_data)
        except ValidationError as e:
            self.throw_error(http_code=self.code.BAD_REQUEST, err=e.messages)

        wagers = services.find_wagers(uuid=uuid)
        if not wagers.total:
            self.throw_error(http_code=self.code.NOT_FOUND)

        party = services.init_party(name=data['name'], wager=wagers.items[0])
        party = services.save_party(party=party)
        return DataResponse(
            data={
                'parties': services.dump_party(
                    schema=dump_schema,
                    party=party
                )
            }
        )
