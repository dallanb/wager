import logging
from http import HTTPStatus

from .base import Base
from ..models import Payout as PayoutModel


class Payout(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.payout_model = PayoutModel

    def find(self, **kwargs):
        return Base.find(self, model=self.payout_model, **kwargs)

    def create(self, **kwargs):
        payout = self.init(model=self.payout_model, **kwargs)
        return self.save(instance=payout)

    def update(self, uuid, **kwargs):
        parties = self.find(uuid=uuid)
        if not parties.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        payout = self.assign_attr(instance=parties.items[0], attr=kwargs)
        return self.save(instance=payout)
