import pytest
from src import services, models


@pytest.fixture
def create_stake():
    def _method(participant_uuid, **kwargs):
        base = services.Base()
        stake = base.init(model=models.Stake)
        stake.participant_uuid = participant_uuid
        stake.currency = kwargs.get('currency', None)
        stake.amount = kwargs.get('amount', None)

        stake = base.save(instance=stake)
        return stake

    return _method
