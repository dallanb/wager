import logging
from .base import Base
from ..models import Wager as WagerModel


class Wager(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.wager_model = WagerModel

    def add(self, **kwargs):
        wager = self._init(model=self.wager_model, **kwargs)
        return self._add(instance=wager)

    def create(self, **kwargs):
        wager = self._init(model=self.wager_model, **kwargs)
        _ = self.notify(
            topic='wagers',
            value={'uuid': str(wager.uuid)},
            key='wager_created'
        )
        return self._save(instance=wager)

    def find(self, **kwargs):
        return self._find(self, model=self.wager_model, **kwargs)
