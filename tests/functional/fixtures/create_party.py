import pytest
from src import services


@pytest.fixture
def create_party(wager_uuid, name):
    wager_party = services.init_wager_party()
    wager_party.wager_uuid = wager_uuid
    wager_party.name = name

    wager_party.save_wager_party()
    return wager_party
