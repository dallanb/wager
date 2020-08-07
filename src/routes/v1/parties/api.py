from flask import request
from flask_restful import marshal_with
from .schema import *
from ..base import Base
from ....models import Party, Wager
from ....common.response import DataResponse
from ....common.auth import check_user


class PartiesAPI(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    def get(self, uuid):
        parties = self.find(model=Party, uuid=uuid)
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

    @marshal_with(DataResponse.marshallable())
    @check_user
    def put(self, uuid):
        data = self.clean(schema=update_schema, instance=request.get_json())
        parties = self.find(model=Party, uuid=uuid, not_found=self.code.NOT_FOUND)
        party = self.assign_attr(instance=parties.items[0], attr=data)
        party = self.save(instance=party)
        return DataResponse(
            data={
                'parties': self.dump(
                    schema=dump_schema,
                    instance=party
                )
            }
        )


class PartiesListAPI(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    def get(self):
        data = self.clean(schema=fetch_all_schema, instance=request.args)
        parties = self.find(model=Party, **data)
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

    @marshal_with(DataResponse.marshallable())
    @check_user
    def post(self, uuid):
        data = self.clean(schema=create_schema, instance=request.get_json())
        wagers = self.find(model=Wager, uuid=uuid, not_found=self.code.NOT_FOUND)
        party = self.init(model=Party, name=data['name'], wager=wagers.items[0])
        party = self.save(instance=party)
        return DataResponse(
            data={
                'parties': self.dump(
                    schema=dump_schema,
                    instance=party
                )
            }
        )
