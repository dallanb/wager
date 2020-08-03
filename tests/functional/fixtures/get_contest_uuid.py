import pytest
from uuid import uuid4

global_contest_uuid = uuid4()


@pytest.fixture
def get_contest_uuid():
    return global_contest_uuid
