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
        return self._find(model=self.contest_model, **kwargs)

    def add(self, **kwargs):
        contest = self._init(model=self.contest_model, **kwargs)
        return self._add(instance=contest)

    def commit(self):
        return self._commit()

    def create(self, **kwargs):
        contest = self._init(model=self.contest_model, **kwargs)
        return self._save(instance=contest)
