from flask import request
from flask_restful import marshal_with
from .schema import *
from ..base import Base
from ....common.response import DataResponse, MessageResponse
from ....common.auth import check_user
from ....services import Stake, Participant


class StakesAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.stake = Stake()

    @marshal_with(DataResponse.marshallable())
    @check_user
    def put(self, uuid):
        data = self.clean(schema=update_schema, instance=request.get_json())
        stake = self.stake.update(uuid=uuid, **data)
        return DataResponse(
            data={
                'stakes': self.dump(
                    schema=dump_schema,
                    instance=stake
                )
            }
        )

    @marshal_with(MessageResponse.marshallable())
    def delete(self, uuid):
        _ = self.stake.destroy(uuid=uuid)
        return MessageResponse()


class StakesListAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.stake = Stake()
        self.participant = Participant()

    @marshal_with(DataResponse.marshallable())
    @check_user
    def post(self, uuid):
        data = self.clean(schema=create_schema, instance=request.get_json())
        participants = self.participant.find(uuid=uuid)
        if not participants.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        stake = self.stake.create(currency=data['currency'], amount=data['amount'],
                                  participant=participants.items[0])
        return DataResponse(
            data={
                'stakes': self.dump(
                    schema=dump_schema,
                    instance=stake
                )
            }
        )
