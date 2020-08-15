import pytest
from src import services


@pytest.fixture
def create_stake():
    def _method(participant_uuid, **kwargs):
        return services.Stake().create(participant_uuid=participant_uuid, currency=kwargs.get('currency', None),
                                       amount=kwargs.get('amount', None))

    return _method
