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
        except ValidationError:
            self.throw_error(http_code=self.code.BAD_REQUEST)
        wager = services.find_wager(**data)
        total = services.count_wager()
        wager_result = services.dump_wager(wager, many=True)
        _metadata = self.prepare_metadata(total=total, **data)
        return DataResponse(
            data={'_metadata': _metadata, 'wager': wager_result})


class FetchAllSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
