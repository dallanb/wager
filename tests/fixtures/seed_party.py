import pytest

from src import services
from ..helpers import generate_uuid, generate_number


@pytest.fixture(scope="function")
def seed_party():
    # create wager
    wager = services.WagerService().create(status='active')
    # create contest
    _ = services.ContestService().create(contest_uuid=generate_uuid(), buy_in=generate_number(), wager=wager)
    # create party
    party = services.PartyService().create(wager_uuid=wager.uuid)
    return party
