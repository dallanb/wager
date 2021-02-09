import pytest
from ..helpers import generate_uuid, generate_number
from src import services


@pytest.fixture(scope="function")
def seed_stake():
    # create wager
    wager = services.WagerService().create(status='active')
    # create contest
    contest = services.ContestService().create(contest_uuid=generate_uuid(), buy_in=generate_number(), wager=wager)
    # create party
    party = services.PartyService().create(wager_uuid=wager.uuid)
    # create participant
    participant = services.ParticipantService().create(party_uuid=party.uuid, member_uuid=generate_uuid(),
                                                       status='pending')
    # create stake
    stake = services.StakeService().create(participant_uuid=participant.uuid, amount=contest.buy_in)
    return stake
