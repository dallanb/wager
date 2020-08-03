import pytest
import json
from src import app


###########
# Create
###########
@pytest.mark.usefixtures("get_user_uuid")
@pytest.mark.usefixtures("get_contest_uuid")
def test_create_wager(get_user_uuid, get_contest_uuid):
    user_uuid = get_user_uuid()
    contest_uuid = get_contest_uuid()
    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Payload
    payload = {'contest_uuid': contest_uuid}

    # Request
    response = app.test_client().post('/wagers', json=payload,
                                      headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['wagers']['status'] == "pending"
    assert response['data']['wagers']['uuid'] is not None


###########
# Fetch
###########
@pytest.mark.usefixtures("get_user_uuid")
@pytest.mark.usefixtures("get_contest_uuid")
@pytest.mark.usefixtures("create_wager")
def test_fetch_wager(get_user_uuid, get_contest_uuid, create_wager):
    user_uuid = get_user_uuid()
    contest_uuid = get_contest_uuid()

    wager = create_wager(owner_uuid=user_uuid, contest_uuid=contest_uuid)
    wager_uuid = wager

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Request
    response = app.test_client().get(f'/wagers/{wager_uuid}',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['wagers']['uuid'] == wager_uuid


###########
# Fetch All
###########
@pytest.mark.usefixtures("get_user_uuid")
def test_fetch_all_wager(get_user_uuid):
    user_uuid = get_user_uuid()

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Request
    response = app.test_client().get('/wagers',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"


###########
# Update
# Not really valid because there is nothing to update on a Wager
###########
@pytest.mark.usefixtures("get_user_uuid")
@pytest.mark.usefixtures("get_contest_uuid")
@pytest.mark.usefixtures("create_wager")
def test_update_wager(get_user_uuid, get_contest_uuid, create_wager):
    user_uuid = get_user_uuid()
    contest_uuid = get_contest_uuid()

    wager = create_wager(owner_uuid=user_uuid, contest_uuid=contest_uuid)
    wager_uuid = wager

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Payload
    payload = {}

    # Request
    response = app.test_client().put(f'/wagers/{wager_uuid}',
                                     payload=payload,
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['wagers']['uuid'] == wager_uuid


###########
# Destroy
# Not really valid because Wagers should not be deleted
###########
@pytest.mark.usefixtures("get_user_uuid")
@pytest.mark.usefixtures("get_contest_uuid")
@pytest.mark.usefixtures("create_wager")
def test_delete_wager(get_user_uuid, get_contest_uuid, create_wager):
    user_uuid = get_user_uuid()
    contest_uuid = get_contest_uuid()

    wager = create_wager(owner_uuid=user_uuid, contest_uuid=contest_uuid)
    wager_uuid = wager

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Request
    response = app.test_client().delete(f'/wagers/{wager_uuid}',
                                        headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
