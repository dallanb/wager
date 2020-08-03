import pytest
from uuid import uuid4

global_participant_uuid = uuid4()


@pytest.fixture
def get_participant_uuid():
    return global_participant_uuid
