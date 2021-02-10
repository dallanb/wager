import pytest

from src import services


@pytest.fixture(scope="function")
def seed_payout():
    # create wager
    wager = services.WagerService().create(status='active')
    # create contest
    payout = services.PayoutService().create(rank=1, proportion=1.0, wager=wager)
    return payout
