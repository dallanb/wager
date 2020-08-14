import pytest
from src import services, models


@pytest.fixture
def create_wager():
    def _method(owner_uuid, contest_uuid):
        base = services.Base()
        wager = base.init(model=models.Wager, owner_uuid=owner_uuid, status='pending')

        # contest (possibly handle this asynchronously)
        _ = base.init(model=models.Contest, contest_uuid=contest_uuid, wager=wager)

        wager = base.save(instance=wager)
        return wager

    return _method
