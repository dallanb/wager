from flask import request
from flask_restful import marshal_with
from .schema import *
from ..base import Base
from ....common.response import DataResponse
from ....services import PartyService, WagerService


class PartiesAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.party = PartyService()

    @marshal_with(DataResponse.marshallable())
    def get(self, uuid):
        parties = self.party.find(uuid=uuid)
        if not parties.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        return DataResponse(
            data={
                'parties': self.dump(
                    schema=dump_schema,
                    instance=parties.items[0]
                )
            }
        )


class PartiesListAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.party = PartyService()
        self.wager = WagerService()

    @marshal_with(DataResponse.marshallable())
    def get(self):
        data = self.clean(schema=fetch_all_schema, instance=request.args)
        parties = self.party.find(**data)
        return DataResponse(
            data={
                '_metadata': self.prepare_metadata(
                    total_count=parties.total,
                    page_count=len(parties.items),
                    page=data['page'],
                    per_page=data['per_page']
                ),
                'parties': self.dump(
                    schema=dump_many_schema,
                    instance=parties.items,
                    params={
                        'expand': data['expand'],
                        'include': data['include']
                    }
                )
            }
        )