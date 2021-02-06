from flask_restful import marshal_with

from .schema import *
from ..base import Base
from ....common import DataResponse
from ....services import ContestService, PartyService, PayoutService


class ContestsCompleteAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.contest = ContestService()
        self.payout = PayoutService()
        self.party = PartyService()

    @marshal_with(DataResponse.marshallable())
    def get(self, contest_uuid):
        contests = self.contest.find(contest_uuid=contest_uuid)
        if not contests.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        contest = contests.items[0]
        wager = contest.wager
        buy_in = contest.buy_in

        # find the payouts proportions for this contest
        payouts = self.payout.find(wager_uuid=wager.uuid)
        # find the number of parties
        parties = self.party.find(wager_uuid=wager.uuid)
        parties_total = parties.total
        # return the payouts for placers
        total_payout = buy_in * parties_total
        party_payouts = {payout.rank: payout.proportion * total_payout for payout in payouts.items}
        payout_proportions = {payout.rank: payout.proportion for payout in payouts.items}
        return DataResponse(
            data={
                'contest': self.dump(
                    schema=dump_complete_schema,
                    instance={
                        'uuid': contest_uuid,
                        'parties': parties_total,
                        'total_payout': total_payout,
                        'buy_in': buy_in,
                        'party_payouts': party_payouts,
                        'payout_proportions': payout_proportions
                    }
                )
            }
        )
