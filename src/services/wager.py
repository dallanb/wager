import logging
import math
from http import HTTPStatus

from .base import Base
from ..decorators import wager_notification
from ..models import Wager as WagerModel
from ..services import PayoutService


class Wager(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.wager_model = WagerModel
        self.payout_service = PayoutService()

    @wager_notification(operation='create')
    def create(self, **kwargs):
        wager = self._init(model=self.wager_model, **kwargs)
        return self._save(instance=wager)

    def find(self, **kwargs):
        return self._find(model=self.wager_model, **kwargs)

    def update(self, uuid, **kwargs):
        wagers = self.find(uuid=uuid)
        if not wagers.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=wagers.items[0], **kwargs)

    def apply(self, instance, **kwargs):
        # if wager status is being updated we will trigger a notification
        wager = self._assign_attr(instance=instance, attr=kwargs)
        return self._save(instance=wager)

    # pass in an ordered list of payout proportions to be inserted into the payout table as individual rows
    def validate_and_create_payout(self, instance, payout_list):
        if not math.fsum(payout_list) == 1.0:
            self.error(code=HTTPStatus.BAD_REQUEST)
        if self.payout_service.find(wager_uuid=instance.uuid).total:
            self.error(code=HTTPStatus.BAD_REQUEST, msg='payout can only be added once for a wager')

        payouts = []
        for i, payout in enumerate(payout_list):
            new_payout = self.payout_service.create(rank=i + 1, proportion=payout, wager=instance)
            payouts.append(new_payout)
        return payouts

    # check if payout associated with this wager instance is still valid
    def check_payout(self, instance):
        parties = instance.parties
        payouts = self.payout_service.find(wager=instance, sort_by='rank.asc')
        payouts_total = payouts.total
        parties_total = len(parties)

        # there are more payouts than there are people competing in the contest
        # the goal here is to redistribute the proportion of the total payout to the remaining parties
        if payouts_total > parties_total:
            valid_payouts = payouts.items[:parties_total]
            invalid_payouts = payouts.items[parties_total:]
            invalid_prop_sum = math.fsum(invalid_payout.proportion for invalid_payout in invalid_payouts)
            invalid_prop_avg = invalid_prop_sum / parties_total
            for valid_payout in valid_payouts:
                self._assign_attr(instance=valid_payout,
                                  attr={'proportion': valid_payout.proportion + invalid_prop_avg})
            for invalid_payout in invalid_payouts:
                self._delete(instance=invalid_payout)
            self._commit()
