from flask import request
from flask_restful import marshal_with
from .schema import *
from ..base import Base
from ....common.response import DataResponse
from ....services import Wager


class WagersAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.wager = Wager()

    @marshal_with(DataResponse.marshallable())
    def get(self, uuid):
        wagers = self.wager.find(uuid=uuid)
        if not wagers.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        return DataResponse(
            data={
                'wagers': self.dump(
                    schema=dump_schema,
                    instance=wagers.items[0]
                )
            }
        )


class WagersListAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.wager = Wager()

    @marshal_with(DataResponse.marshallable())
    def get(self):
        data = self.clean(schema=fetch_all_schema, instance=request.args)
        wagers = self.wager.find(**data)
        return DataResponse(
            data={
                '_metadata': self.prepare_metadata(
                    total_count=wagers.total,
                    page_count=len(wagers.items),
                    page=data['page'],
                    per_page=data['per_page']),
                'wagers': self.dump(
                    schema=dump_many_schema,
                    instance=wagers.items,
                    params={
                        'include': data['include']
                    }
                )
            }
        )
