import json

import pytest

from src import app
from tests.functional.helpers import generate_name, generate_number


###########
# Create
###########
@pytest.mark.parametrize("party_name", [generate_name()])
@pytest.mark.parametrize("stake_amount", [generate_number()])
def test_create_stake(party_name, stake_amount, get_user_uuid, get_contest_uuid,
                      get_participant_uuid,
                      create_wager,
                      create_party,
                      create_participant):
    user_uuid = get_user_uuid()
    contest_uuid = get_contest_uuid()
    participant_uuid = get_participant_uuid()
    wager = create_wager(contest_uuid=contest_uuid)
    wager_uuid = wager.uuid
    wager_party = create_party(wager_uuid=wager_uuid, name=party_name)
    party_uuid = wager_party.uuid
    wager_party_participant = create_participant(party_uuid=party_uuid, user_uuid=participant_uuid)
    participant_uuid = wager_party_participant.uuid

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Payload
    payload = {'amount': stake_amount}

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
# Update
###########
@pytest.mark.parametrize("party_name", [generate_name()])
@pytest.mark.parametrize("stake_amount", [generate_number()])
def test_update_stake(party_name, stake_amount, get_user_uuid, get_contest_uuid,
                      get_participant_uuid,
                      create_wager,
                      create_party,
                      create_participant,
                      create_stake):
    user_uuid = get_user_uuid()
    contest_uuid = get_contest_uuid()
    wager = create_wager(contest_uuid=contest_uuid)
    wager_uuid = wager.uuid
    party = create_party(wager_uuid=wager_uuid, name=party_name)
    party_uuid = party.uuid
    participant = create_participant(party_uuid=party_uuid, user_uuid=user_uuid)
    participant_uuid = participant.uuid
    stake = create_stake(participant_uuid=participant_uuid, amount=stake_amount)
    stake_uuid = stake.uuid

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Payload
    payload = {'amount': 49.99}

    # Request
    response = app.test_client().put(f'/stakes/{stake_uuid}',
                                     json=payload,
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['stakes']['uuid'] == str(stake_uuid)


###########
# Destroy
###########
@pytest.mark.parametrize("party_name", [generate_name()])
@pytest.mark.parametrize("stake_amount", [generate_number()])
def test_destroy_stake(party_name, stake_amount, get_user_uuid, get_contest_uuid,
                       get_participant_uuid,
                       create_wager,
                       create_party,
                       create_participant,
                       create_stake):
    user_uuid = get_user_uuid()
    contest_uuid = get_contest_uuid()
    wager = create_wager(contest_uuid=contest_uuid)
    wager_uuid = wager.uuid
    party = create_party(wager_uuid=wager_uuid, name=party_name)
    party_uuid = party.uuid
    participant = create_participant(party_uuid=party_uuid, user_uuid=user_uuid)
    participant_uuid = participant.uuid
    stake = create_stake(participant_uuid=participant_uuid, amount=stake_amount)
    stake_uuid = stake.uuid

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Request
    response = app.test_client().delete(f'/stakes/{stake_uuid}',
                                        headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
