import pytest
from src import services


@pytest.fixture
def create_stake():
    def _method(participant_uuid, **kwargs):
        stake = services.init_stake()
        stake.participant_uuid = participant_uuid
        stake.currency = kwargs.get('currency', None)
        stake.amount = kwargs.get('amount', None)

        stake = services.save_stake(stake)
        return stake

    return _method
