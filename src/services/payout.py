import logging

from .base import Base
from ..models import Payout as PayoutModel


class Payout(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.payout_model = PayoutModel

    def find(self, **kwargs):
        return self._find(model=self.payout_model, **kwargs)

    # this create should not be directly called and instead from the Wager service
    def create(self, **kwargs):
        payout = self._init(model=self.payout_model, **kwargs)
        return self._save(instance=payout)
