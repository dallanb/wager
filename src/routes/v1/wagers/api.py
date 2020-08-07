from flask import request, g
from flask_restful import marshal_with
from marshmallow import ValidationError
from .schema import *
from ..base import Base
from ....common.response import DataResponse
from ....common.auth import check_user
from .... import services


class WagersAPI(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    def get(self, uuid):
        wagers = services.find_wagers(uuid=uuid)
        if not wagers.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        return DataResponse(
            data={
                'wagers': services.dump_wager(
                    schema=dump_schema,
                    wager=wagers.items[0]
                )
            }
        )


class WagersListAPI(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    def get(self):
        try:
            data = services.clean_wager(schema=fetch_all_schema, wager=request.args)
        except ValidationError as e:
            self.throw_error(http_code=self.code.BAD_REQUEST, err=e.messages)

        wagers = services.find_wagers(**data)
        return DataResponse(
            data={
                '_metadata': self.prepare_metadata(
                    total_count=wagers.total,
                    page_count=len(wagers.items),
                    page=data['page'],
                    per_page=data['per_page']),
                'wagers': services.dump_wager(
                    schema=dump_many_schema,
                    wager=wagers.items,
                    params={
                        'include': data['include']
                    }
                )
            }
        )

    @marshal_with(DataResponse.marshallable())
    @check_user
    def post(self):
        json_data = request.get_json()
        try:
            contest_data = services.clean_wager(schema=create_schema, wager=json_data)
        except ValidationError as e:
            self.throw_error(http_code=self.code.BAD_REQUEST, err=e.messages)

        # contest
        wager = services.init_wager(status='pending', owner_uuid=g.user)
        contest = services.init_contest(contest_uuid=contest_data['contest_uuid'], wager=wager)
        wager = services.save_wager(wager)
        contest = services.save_contest(contest=contest)
        return DataResponse(
            data={
                'wagers': services.dump_wager(
                    schema=dump_schema,
                    wager=wager
                )
            }
        )
