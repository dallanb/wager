import logging
from .base import Base
from ..models import Wager as WagerModel


class Wager(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.wager_model = WagerModel()

    def handle_event(self, key, data):
        self.logger.info(key)
        self.logger.info(data)
        return key

    def create(self, **kwargs):
        wager = self.init(model=self.wager_model, **kwargs)
        return self.save(instance=wager)

    def find(self, **kwargs):
        return self.find(model=self.wager_model, **kwargs)
