import logging

from .base import Base
from ..models import Party as PartyModel


class Party(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.party_model = PartyModel

    def find(self, **kwargs):
        return self._find(model=self.party_model, **kwargs)

    def add(self, **kwargs):
        party = self._init(model=self.party_model, **kwargs)
        return self._add(instance=party)

    def commit(self):
        return self._commit()

    def create(self, **kwargs):
        party = self._init(model=self.party_model, **kwargs)
        return self._save(instance=party)

    def rollback(self):
        return self._rollback()
