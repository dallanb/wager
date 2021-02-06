import pytest
from src import services


@pytest.fixture
def create_wager():
    def _method(contest_uuid, buy_in):
        wager = services.WagerService().create(status='active')
        # contest (possibly handle this asynchronously)
        _ = services.ContestService().create(contest_uuid=contest_uuid, buy_in=buy_in, wager=wager)
        return wager

    return _method
