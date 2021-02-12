import pytest

from src import services


@pytest.fixture(scope="function")
def seed_payouts():
    # create wager
    wager = services.WagerService().create(status='active')
    # create contest
    payouts = services.WagerService().validate_and_create_payout(instance=wager, payout_list=[0.75, 0.25])
    return payouts
