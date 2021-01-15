import pytest
from src import services


@pytest.fixture
def create_wager():
    def _method(owner_uuid, contest_uuid):
        wager = services.WagerService().create(owner_uuid=owner_uuid, status='pending')
        # contest (possibly handle this asynchronously)
        _ = services.ContestService().create(contest_uuid=contest_uuid, wager=wager)
        return wager

    return _method
