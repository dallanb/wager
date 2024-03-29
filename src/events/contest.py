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
            contest = self.contest_service.create(contest_uuid=data['contest_uuid'], buy_in=data['buy_in'])
            wager = self.wager_service.create(status='active', contest=contest)
            self.wager_service.validate_and_create_payout(instance=wager, payout_list=data['payout'])
            party = self.party_service.add(wager=wager)
            participant = self.participant_service.add(member_uuid=data['member_uuid'],
                                                       status='active', party=party)
            _ = self.stake_service.create(amount=data['buy_in'], participant=participant)

        elif key == 'participant_active':
            self.logger.info('participant active')
            wagers = self.wager_service.find(contest_uuid=data['contest_uuid'])
            if wagers.total:
                wager = wagers.items[0]
                party = self.party_service.add(wager=wager)
                participant = self.participant_service.add(member_uuid=data['member_uuid'],
                                                           status='active', party=party)
                _ = self.stake_service.create(amount=wager.contest.buy_in, participant=participant)
        elif key == 'participant_inactive':
            self.logger.info('participant inactive')
        elif key == 'contest_ready':
            self.logger.info('contest ready')
            wagers = self.wager_service.find(contest_uuid=data['uuid'])
            if wagers.total:
                self.wager_service.check_payout(instance=wagers.items[0])
        elif key == 'contest_inactive':
            self.logger.info('contest inactive')
            wagers = self.wager_service.find(contest_uuid=data['uuid'])
            if wagers.total:
                wager = wagers.items[0]
                self.wager_service.apply(instance=wager, status='inactive')
                parties = wager.parties
                for party in parties:
                    participants = party.participants
                    for participant in participants:
                        if participant.status.name == 'active':
                            self.participant_service.apply(instance=participant, status='inactive')
