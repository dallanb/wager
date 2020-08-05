from flask import request
from flask_restful import marshal_with
from marshmallow import ValidationError
from .. import Base
from .... import services
from ....common import DataResponse
from ....schemas import fetch_all_stake_schema


class FetchAll(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    def get(self):
        try:
            data = fetch_all_stake_schema.load(request.args)
        except ValidationError as e:
            self.throw_error(http_code=self.code.BAD_REQUEST, err=e.messages)
        stakes = services.find_stake(**data)
        total = services.count_stake()
        stake_result = services.dump_stakes(stakes=stakes, many=True)
        _metadata = self.prepare_metadata(total=total, **data)
        return DataResponse(
            data={'_metadata': _metadata, 'stakes': stake_result})
