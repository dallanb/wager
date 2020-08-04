import pytest
import json
from tests.functional.helpers import generate_name, generate_uuid
from src import app


###########
# Create
###########
@pytest.mark.parametrize("party_name", [generate_name()])
def test_create_participant(party_name, get_user_uuid, get_contest_uuid, get_participant_uuid, create_wager,
                            create_party):
    user_uuid = get_user_uuid()
    contest_uuid = get_contest_uuid()
    wager = create_wager(owner_uuid=user_uuid, contest_uuid=contest_uuid)
    wager_uuid = wager.uuid
    party = create_party(wager_uuid=wager_uuid, name=party_name)
    party_uuid = party.uuid

    participant_user_uuid = generate_uuid()

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Payload
    payload = {'user_uuid': participant_user_uuid}

    # Request
    response = app.test_client().post(f'parties/{party_uuid}/participants', json=payload,
                                      headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['participants']['status'] == 'pending'
    assert response['data']['participants']['uuid'] is not None


###########
# Fetch
###########
@pytest.mark.parametrize("party_name", [generate_name()])
def test_fetch_participant(party_name, get_user_uuid, get_contest_uuid, get_participant_uuid, create_wager,
                           create_party, create_participant):
    user_uuid = get_user_uuid()
    contest_uuid = get_contest_uuid()
    wager = create_wager(owner_uuid=user_uuid, contest_uuid=contest_uuid)
    wager_uuid = wager.uuid
    party = create_party(wager_uuid=wager_uuid, name=party_name)
    party_uuid = party.uuid
    participant = create_participant(party_uuid=party_uuid, user_uuid=user_uuid)
    participant_uuid = participant.uuid

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Request
    response = app.test_client().get(f'/participants/{participant_uuid}',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['participants']['uuid'] == str(participant_uuid)


###########
# Fetch All
###########
def test_fetch_all_participant(get_user_uuid):
    user_uuid = get_user_uuid()

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Request
    response = app.test_client().get('/participants',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
