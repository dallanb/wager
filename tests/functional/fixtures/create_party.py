import pytest
from src import services


@pytest.fixture
def create_party():
    def _method(wager_uuid):
        return services.PartyService().create(wager_uuid=wager_uuid)

    return _method
