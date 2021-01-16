import logging

from .base import Base
from ..external import Contest as ContestExternal
from ..models import Contest as ContestModel


class Contest(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.contest_external = ContestExternal()
        self.contest_model = ContestModel

    def find(self, **kwargs):
        return Base.find(self, model=self.contest_model, **kwargs)

    def create(self, **kwargs):
        contest = self.init(model=self.contest_model, **kwargs)
        return self.save(instance=contest)

    # add caching to this method to avoid chatty api
    def fetch_contest(self, uuid, params=None):
        res = self.contest_external.get_contest(uuid=uuid, params=params)
        return res['data']['contests']
