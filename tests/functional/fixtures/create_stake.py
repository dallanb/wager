import pytest

from src import services


@pytest.fixture
def create_stake():
    def _method(participant_uuid, **kwargs):
        return services.StakeService().create(participant_uuid=participant_uuid, amount=kwargs.get('amount', None))

    return _method
