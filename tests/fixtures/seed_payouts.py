import pytest

from src import services
from tests.helpers import generate_number, generate_uuid


@pytest.fixture(scope="function")
def seed_payouts():
    # create wager
    wager = services.WagerService().create(status='active')
    # create contest
    _ = services.ContestService().create(contest_uuid=generate_uuid(), buy_in=generate_number(), wager=wager)
    # create payout
    payouts = services.WagerService().validate_and_create_payout(instance=wager, payout_list=[0.75, 0.25])
    return payouts
