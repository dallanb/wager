import pytest
import json
from flask_seeder import generator
from src import app


###########
# Create
###########
@pytest.mark.parametrize("party_name", [generator.Name()])
@pytest.mark.parametrize("wager_currency", ["CAD"])
@pytest.mark.parametrize("wager_amount", [generator.Integer(start=20, end=100)])
@pytest.mark.usefixtures("get_user_uuid")
@pytest.mark.usefixtures("get_contest_uuid")
@pytest.mark.usefixtures("get_participant_uuid")
@pytest.mark.usefixtures("create_wager")
@pytest.mark.usefixtures("create_party")
@pytest.mark.usefixtures("create_participant")
def test_create_stake(party_name, wager_currency, wager_amount, get_user_uuid, get_contest_uuid,
                      get_participant_uuid,
                      create_wager,
                      create_party,
                      create_participant):
    user_uuid = get_user_uuid()
    contest_uuid = get_contest_uuid()
    participant_uuid = get_participant_uuid()
    wager = create_wager(user_uuid=user_uuid, contest_uuid=contest_uuid)
    wager_uuid = wager.uuid
    wager_party = create_party(wager_uuid=wager_uuid, party_name=party_name)
    party_uuid = wager_party.uuid
    wager_party_participant = create_participant(party_uuid=party_uuid, participant_uuid=participant_uuid)
    participant_uuid = wager_party_participant.uuid

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Payload
    payload = {'currency': wager_currency, 'amount': wager_amount}

    # Request
    response = app.test_client().post(f'/participants/{participant_uuid}/stakes',
                                      json=payload,
                                      headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['stakes']['uuid'] is not None
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
