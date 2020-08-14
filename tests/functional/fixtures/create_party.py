import pytest
from src import services, models


@pytest.fixture
def create_party():
    def _method(wager_uuid, name):
        base = services.Base()
        party = base.init(model=models.Party, wager_uuid=wager_uuid, name=name)
        party = base.save(instance=party)
        return party

    return _method
