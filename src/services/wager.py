import logging
from http import HTTPStatus

from .base import Base
from ..models import Wager as WagerModel
from ..services import PayoutService


class Wager(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.wager_model = WagerModel
        self.payout_service = PayoutService()

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
        return self._find(model=self.wager_model, **kwargs)

    def update(self, uuid, **kwargs):
        wagers = self.find(uuid=uuid)
        if not wagers.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=wagers.items[0], **kwargs)

    def apply(self, instance, **kwargs):
        wager = self._assign_attr(instance=instance, attr=kwargs)
        return self._save(instance=wager)

    # pass in an ordered list of payout proportions to be inserted into the payout table as individual rows
    def validate_and_create_payout(self, instance, payout_list):
        if not sum(payout_list) == 1.0:
            self.error(code=HTTPStatus.BAD_REQUEST)
        if self.payout_service.find(wager_uuid=instance.uuid).total:
            self.error(code=HTTPStatus, msg='payout can only be added once for a wager')

        payouts = []
        for i, payout in enumerate(payout_list):
            new_payout = self.payout_service.create(rank=i + 1, proportion=payout, wager=instance)
            payouts.append(new_payout)
        return payouts
