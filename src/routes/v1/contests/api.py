from flask_restful import marshal_with
from ..base import Base
from ....common import DataResponse
from ....services import ContestService


class ContestsCompleteAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.contest = ContestService()

    @marshal_with(DataResponse.marshallable())
    def get(self, uuid):
        contests = self.contest.find(uuid=uuid, include=[])
        if not contests.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        contest = contests.items[0]
        return DataResponse(message='pong')
