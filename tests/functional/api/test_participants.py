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
@pytest.mark.usefixtures("get_participant_uuid")
@pytest.mark.usefixtures("create_wager")
@pytest.mark.usefixtures("create_party")
def test_create_participant(party_name, get_user_uuid, get_contest_uuid, get_participant_uuid, create_wager,
                            create_party):
    user_uuid = get_user_uuid()
    contest_uuid = get_contest_uuid()
    wager = create_wager(owner_uuid=user_uuid, contest_uuid=contest_uuid)
    wager_uuid = wager.uuid
    wager_party = create_party(wager_uuid=wager_uuid, party_name=party_name)
    party_uuid = wager_party.uuid

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Payload
    payload = {'user_uuid': get_participant_uuid}

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

###########
# Fetch All
###########

###########
# Update
###########

###########
# Destroy
###########
