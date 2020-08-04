import pytest
from src import services


@pytest.fixture
def create_wager():
    def _method(owner_uuid, contest_uuid):
        wager = services.init_wager(owner_uuid=owner_uuid, status='pending')

        # contest (possibly handle this asynchronously)
        _ = services.init_contest(contest_uuid=contest_uuid, wager=wager)

        wager = services.save_wager(wager)
        return wager

    return _method
