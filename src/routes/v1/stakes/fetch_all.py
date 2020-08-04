from flask import request
from flask_restful import marshal_with
from marshmallow import fields, Schema, ValidationError
from .. import Base
from .... import services
from ....common import DataResponse


class FetchAll(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    def get(self):
        try:
            data = FetchAllSchema().load(request.args)
        except ValidationError as e:
            self.throw_error(http_code=self.code.BAD_REQUEST, err=e.messages)
        stake = services.find_stake(**data)
        total = services.count_stake()
        stake_result = services.dump_stake(stake=stake, many=True)
        _metadata = self.prepare_metadata(total=total, **data)
        return DataResponse(
            data={'_metadata': _metadata, 'stakes': stake_result})


class FetchAllSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
