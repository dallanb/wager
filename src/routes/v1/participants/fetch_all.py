from flask import request
from flask_restful import marshal_with
from marshmallow import ValidationError
from .. import Base
from .... import services
from ....common import DataResponse
from ....schemas import fetch_all_participant_schema


class FetchAll(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    def get(self):
        try:
            data = fetch_all_participant_schema.load(request.args)
        except ValidationError as e:
            self.throw_error(http_code=self.code.BAD_REQUEST, err=e.messages)
        participants = services.find_participant(**data)
        total = services.count_participant()
        participant_result = services.dump_participants(participants=participants, many=True)
        _metadata = self.prepare_metadata(total=total, **data)
        return DataResponse(
            data={'_metadata': _metadata, 'participant': participant_result})
