import logging

from ..services import ContestService, StakeService, WagerService, ParticipantService, PartyService


class Contest:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.contest_service = ContestService()
        self.wager_service = WagerService()
        self.participant_service = ParticipantService()
        self.party_service = PartyService()
        self.stake_service = StakeService()

    def handle_event(self, key, data):
        if key == 'owner_active':
            self.logger.info('owner active')
            wager = self.wager_service.create(status='active')
            _ = self.contest_service.create(contest_uuid=data['contest_uuid'], buy_in=data['buy_in'],
                                            wager=wager)
            self.wager_service.validate_and_create_payout(instance=wager, payout_list=data['payout'])
            party = self.party_service.add(wager=wager)
            participant = self.participant_service.add(member_uuid=data['member_uuid'],
                                                       status='active', party=party)
            _ = self.stake_service.create(amount=data['buy_in'], participant=participant)

        elif key == 'participant_active':
            self.logger.info('participant active')
            contests = self.contest_service.find(contest_uuid=data['contest_uuid'])
            if contests.total:
                party = self.party_service.add(wager=contests.items[0].wager)
                participant = self.participant_service.add(member_uuid=data['member_uuid'],
                                                           status='active', party=party)
                _ = self.stake_service.create(amount=contests.items[0].buy_in, participant=participant)
