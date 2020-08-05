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
        wager = services.find_wager_by_uuid(uuid=uuid)
        if not wager:
            self.throw_error(http_code=self.code.NOT_FOUND)
        wager_result = services.dump_wager(schema=dump_schema, wager=wager)
        return DataResponse(data={'wagers': wager_result})


class WagersListAPI(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    def get(self):
        try:
            data = services.clean_wager(schema=fetch_all_schema, wager=request.args)
        except ValidationError as e:
            self.throw_error(http_code=self.code.BAD_REQUEST, err=e.messages)
        wagers = services.find_wager(**data)
        total = services.count_wager()
        wager_result = services.dump_wager(schema=dump_many_schema, wager=wagers)
        _metadata = self.prepare_metadata(total=total, **data)
        return DataResponse(
            data={'_metadata': _metadata, 'wagers': wager_result})

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
        wager_result = services.dump_wager(schema=dump_schema, wager=wager)
        return DataResponse(data={'wagers': wager_result})
