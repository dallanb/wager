import pytest
from uuid import uuid4

global_user_uuid = uuid4()


@pytest.fixture
def get_user_uuid():
    def _method():
        return global_user_uuid

    return _method
