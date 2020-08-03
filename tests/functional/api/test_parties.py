import pytest
import json
from flask_seeder import generator
from src import app


###########
# Create
###########
@pytest.mark.parametrize("party_name", [generator.Name()])
@pytest.mark.usefixtures("get_user_uuid")
@pytest.mark.usefixtures("get_contest_uuid")
@pytest.mark.usefixtures("create_wager")
def test_create_party(party_name, get_user_uuid, get_contest_uuid, create_wager):
    user_uuid = get_user_uuid()
    contest_uuid = get_contest_uuid()
    wager = create_wager(owner_uuid=user_uuid, contest_uuid=contest_uuid)
    uuid = wager.uuid

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Payload
    payload = {'name': party_name}

    # Request
    response = app.test_client().post(f'/wagers/{uuid}/parties', json=payload,
                                      headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['parties']['name'] == party_name
    assert response['data']['parties']['uuid'] is not None


###########
# Fetch
###########
@pytest.mark.parametrize("party_name", [generator.Name()])
@pytest.mark.usefixtures("get_user_uuid")
@pytest.mark.usefixtures("get_contest_uuid")
@pytest.mark.usefixtures("create_wager")
@pytest.mark.usefixtures("create_party")
def test_fetch_party(party_name, get_user_uuid, get_contest_uuid, create_wager, create_party):
    user_uuid = get_user_uuid()
    contest_uuid = get_contest_uuid()

    wager = create_wager(owner_uuid=user_uuid, contest_uuid=contest_uuid)
    wager_uuid = wager

    wager_party = create_party(wager_uuid=wager_uuid, party_name=party_name)
    party_uuid = wager_party.uuid

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Request
    response = app.test_client().get(f'/parties/{party_uuid}',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['parties']['uuid'] == party_uuid


###########
# Fetch All
###########
@pytest.mark.usefixtures("get_user_uuid")
def test_fetch_all_party(get_user_uuid):
    user_uuid = get_user_uuid()

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Request
    response = app.test_client().get('/parties',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
###########
# Update
###########

###########
# Destroy
###########
