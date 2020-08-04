import pytest
from src import services


@pytest.fixture
def create_party():
    def _method(wager_uuid, name):
        party = services.init_party(wager_uuid=wager_uuid, name=name)
        party = services.save_party(party=party)
        return party

    return _method
