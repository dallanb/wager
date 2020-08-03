import pytest
from src import services


@pytest.fixture
def create_wager(owner_uuid, contest_uuid):
    wager = services.init_wager()
    wager.owner_uuid = owner_uuid

    # status
    status = services.find_wager_status_by_enum('pending')
    wager.status_uuid = status.uuid

    # contest (possibly handle this asynchronously)
    wager_contest = services.init_wager_contest()
    wager_contest.contest_uuid = contest_uuid
    services.save_wager_contest(wager_contest)

    wager = services.save_wager(wager)
    return wager
