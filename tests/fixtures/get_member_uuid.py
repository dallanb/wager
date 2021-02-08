import pytest
from uuid import uuid4

global_member_uuid = uuid4()


@pytest.fixture
def get_member_uuid():
    def _method():
        return global_member_uuid

    return _method
