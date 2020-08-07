from flask import request
from flask_restful import marshal_with
from .schema import *
from ..base import Base
from ....common.response import DataResponse, MessageResponse
from ....common.auth import check_user
from ....models import Stake, Participant


class StakesAPI(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    @check_user
    def put(self, uuid):
        data = self.clean(schema=update_schema, instance=request.get_json())
        stakes = self.find(model=Stake, uuid=uuid, not_found=self.code.NOT_FOUND)
        stake = self.assign_attr(instance=stakes.items[0], attr=data)
        stake = self.save(instance=stake)
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
        stakes = self.find(model=Stake, uuid=uuid, not_found=self.code.NOT_FOUND)
        _ = self.destroy(instance=stakes.items[0])
        return MessageResponse()


class StakesListAPI(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    @check_user
    def post(self, uuid):
        data = self.clean(schema=create_schema, instance=request.get_json())
        participants = self.find(model=Participant, uuid=uuid, not_found=self.code.NOT_FOUND)
        stake = self.init(model=Stake, currency=data['currency'], amount=data['amount'],
                          participant=participants.items[0])
        stake = self.save(instance=stake)
        return DataResponse(
            data={
                'stakes': self.dump(
                    schema=dump_schema,
                    instance=stake
                )
            }
        )
