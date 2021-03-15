import pytest

from src import services


@pytest.fixture(scope="function")
def seed_wager():
    # create contest
    pytest.contest = services.ContestService().create(contest_uuid=pytest.contest_uuid, buy_in=pytest.buy_in)
    # create wager
    pytest.wager = services.WagerService().create(status='active', contest=pytest.contest)
    return pytest.wager
