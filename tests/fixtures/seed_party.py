import pytest

from src import services


@pytest.fixture(scope="function")
def seed_party():
    # create party
    pytest.party = services.PartyService().create(wager_uuid=pytest.wager.uuid)
    return pytest.party
