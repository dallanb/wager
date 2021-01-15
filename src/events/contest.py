import logging

from ..external import Contest as ContestExternal
from ..services import ContestService, WagerService, PayoutService


class Contest:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.contest_service = ContestService()
        self.wager_service = WagerService()
        self.payout_service = PayoutService()
        self.contest_external = ContestExternal()

    def handle_event(self, key, data):
        if key == 'wager_created':
            self.logger.info('wager created')
            wager = self.wager_service.create(status='active')
            _ = self.contest_service.create(contest_uuid=data['uuid'], buy_in=data['buy_in'],
                                            wager=wager)
            for i, payout in enumerate(data['payout']):
                _ = self.payout_service.create(rank=i + 1, proportion=payout, wager=wager)

        elif key == 'contest_ready' or key == 'contest_active' or key == 'contest_inactive' or key == 'contest_completed':
            self.logger.info('contest updated')
        if key == 'contest_ready':
            self.logger.info('contest ready')
            contest = self.contest_external.get_contest(uuid=data['uuid'], )

