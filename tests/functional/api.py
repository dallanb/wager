import json
import pytest
from flask_seeder import generator
from uuid import uuid4
from src import app, services, common

# pytest --disable-pytest-warnings -s

pytest.wagers = services.find_wager()
global_user_uuid = uuid4()
global_participant_uuid = uuid4()
global_contest_uuid = uuid4()
pytest.course = services.find_course_by_golf_canada_id(golf_canada_id=19679)  # northlands


##############
# Fixtures
##############
@pytest.fixture
def get_user_uuid():
    return global_user_uuid


@pytest.fixture
def get_contest_uuid():
    return global_contest_uuid


@pytest.fixture
def get_participant_uuid():
    return global_participant_uuid


@pytest.fixture
def create_wager(user_uuid, contest_uuid):
    wager = services.init_wager()
    wager.owner_uuid = user_uuid

    # status
    status = services.find_wager_status_by_enum('pending')
    wager.status_uuid = status.uuid

    # contest (possibly handle this asynchronously)
    wager_contest = services.init_wager_contest()
    wager_contest.contest_uuid = contest_uuid
    services.save_wager_contest(wager_contest)

    wager = services.save_wager(wager)
    return wager


@pytest.fixture
def create_wager_party(wager_uuid, party_name):
    wager_party = services.init_wager_party()
    wager_party.wager_uuid = wager_uuid
    wager_party.name = party_name

    wager_party.save_wager_party()
    return wager_party


@pytest.fixture
def create_wager_party_participant(party_uuid, participant_uuid):
    wager_party_participant = services.init_wager_party_participant()
    wager_party_participant.party_uuid = party_uuid
    wager_party_participant.user_uuid = participant_uuid

    # status
    status = services.find_wager_party_participant_status_by_enum('pending')
    wager_party_participant.status_uuid = status.uuid

    wager_party_participant.save_wager_party_participant()
    return wager_party_participant


##############
# CREATE
##############
# Create Wager
def test_create_wager(get_user_uuid, get_contest_uuid):
    # Headers
    headers = {'X-Consumer-Custom-ID': get_user_uuid(), 'X-Contest-ID': get_contest_uuid()}

    # Payload
    payload = {}

    # Request
    response = app.test_client().post('/wagers', json=payload,
                                      headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['wagers']['status'] == "pending"
    assert response['data']['wagers']['uuid'] is not None


# Create Wager Party
@pytest.mark.parametrize("party_name", [generator.Name()])
def test_create_wager_party(party_name, get_user_uuid, get_contest_uuid, create_wager):
    user_uuid = get_user_uuid()
    contest_uuid = get_contest_uuid()
    wager = create_wager(user_uuid=user_uuid, contest_uuid=contest_uuid)
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


# Create Wager Party Participant
@pytest.mark.parametrize("party_name", [generator.Name()])
def test_create_wager_party_participant(party_name, get_user_uuid, get_contest_uuid, get_participant_uuid, create_wager,
                                        create_wager_party):
    user_uuid = get_user_uuid()
    contest_uuid = get_contest_uuid()
    wager = create_wager(user_uuid=user_uuid, contest_uuid=contest_uuid)
    wager_uuid = wager.uuid
    wager_party = create_wager_party(wager_uuid=wager_uuid, party_name=party_name)
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


# Create Wager Party Participant
@pytest.mark.parametrize("party_name", [generator.Name()])
@pytest.mark.parametrize("wager_currency", ["CAD"])
@pytest.mark.parametrize("wager_amount", [generator.Integer(start=20, end=100)])
def test_create_wager_party_participant_wager(party_name, wager_currency, wager_amount, get_user_uuid, get_contest_uuid,
                                              get_participant_uuid,
                                              create_wager,
                                              create_wager_party,
                                              create_wager_party_participant):
    user_uuid = get_user_uuid()
    contest_uuid = get_contest_uuid()
    participant_uuid = get_participant_uuid()
    wager = create_wager(user_uuid=user_uuid, contest_uuid=contest_uuid)
    wager_uuid = wager.uuid
    wager_party = create_wager_party(wager_uuid=wager_uuid, party_name=party_name)
    party_uuid = wager_party.uuid
    wager_party_participant = create_wager_party_participant(party_uuid=party_uuid, participant_uuid=participant_uuid)
    participant_uuid = wager_party_participant.uuid

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Payload
    payload = {'currency': wager_currency, 'amount': wager_amount}

    # Request
    response = app.test_client().post(f'/participants/{participant_uuid}/stake',
                                      json=payload,
                                      headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['stakes']['uuid'] is not None


##############
# FETCH
##############
def test_fetch_wager(get_user_uuid, get_contest_uuid, create_wager):
    user_uuid = get_user_uuid()
    contest_uuid = get_contest_uuid()

    wager = create_wager(user_uuid=user_uuid, contest_uuid=contest_uuid)
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


@pytest.mark.parametrize("party_name", [generator.Name()])
def test_fetch_wager_party(party_name, get_user_uuid, get_contest_uuid, create_wager, create_wager_party):
    user_uuid = get_user_uuid()
    contest_uuid = get_contest_uuid()

    wager = create_wager(user_uuid=user_uuid, contest_uuid=contest_uuid)
    wager_uuid = wager

    wager_party = create_wager_party(wager_uuid=wager_uuid, party_name=party_name)
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


def test_fetch_all_wager_party(get_user_uuid, get_contest_uuid):
    user_uuid = get_user_uuid()
    contest_uuid = get_contest_uuid()

    # Headers
    headers = {'X-Consumer-Custom-ID': user_uuid}

    # Request
    response = app.test_client().get('/parties',
                                     headers=headers)

    # Response
    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
