import logging

from .base import Base
from ..decorators import stake_notification
from ..models import Stake as StakeModel


class Stake(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.stake_model = StakeModel

    def find(self, **kwargs):
        return self._find(model=self.stake_model, **kwargs)

    @stake_notification(operation='create')
    def create(self, **kwargs):
        stake = self._init(model=self.stake_model, **kwargs)
        return self._save(instance=stake)
