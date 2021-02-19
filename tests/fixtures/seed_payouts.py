import pytest

from src import services


@pytest.fixture(scope="function")
def seed_payouts():
    # create payout
    pytest.payouts = services.WagerService().validate_and_create_payout(instance=pytest.wager,
                                                                        payout_list=pytest.payout)
    return pytest.payouts
