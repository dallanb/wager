import pytest
from src import services


@pytest.fixture
def create_party():
    def _method(wager_uuid, name):
        return services.Party().create(wager_uuid=wager_uuid, name=name)

    return _method
