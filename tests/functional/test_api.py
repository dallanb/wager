import json
import pytest
from uuid import uuid4
from src import app, services, common

# pytest --disable-pytest-warnings -s

pytest.wagers = services.find_wager()
pytest.owner = uuid4()


def test_ping():
    response = app.test_client().get('/ping')

    assert response.status_code == 200
    assert b'pong' in response.data


# fetch all
def test_fetch_all_wager():
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert b'OK' in response.data


def test_fetch_all_wager_paginate_0():
    response = app.test_client().get('/?page=1&per_page=10')

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == 'OK'
    assert response['data']['_metadata']['total'] == 5
    assert response['data']['_metadata']['page'] == 1
    assert response['data']['_metadata']['per_page'] == 10
    assert len(response['data']['wager']) > 0


def test_fetch_all_wager_paginate_1():
    response = app.test_client().get('/?page=2&per_page=10')

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == 'OK'
    assert response['data']['_metadata']['total'] == 5
    assert response['data']['_metadata']['page'] == 2
    assert response['data']['_metadata']['per_page'] == 10
    assert len(response['data']['wager']) == 0


def test_fetch_all_wager_invalid_paginate_0():
    response = app.test_client().get('/?page=a&per_page=b')

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['data'] is None
    assert response['err']['page'][0] == "Not a valid integer."
    assert response['err']['per_page'][0] == "Not a valid integer."


def test_fetch_all_wager_invalid_paginate_1():
    response = app.test_client().get('/?rage=2&per_rage=10')

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['data'] is None
    assert response['err']['rage'][0] == "Unknown field."
    assert response['err']['per_rage'][0] == "Unknown field."


# fetch
@pytest.mark.parametrize("uuid", [wager.uuid for wager in pytest.wagers])
def test_fetch_wager(uuid):
    response = app.test_client().get(f'/{uuid}')

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == 'OK'
    assert response['data']['wager']['uuid'] == str(uuid)


@pytest.mark.parametrize("uuid", ['12345'])
def test_fetch_wager_invalid_type(uuid):
    response = app.test_client().get(f'/{uuid}')

    assert response.status_code == 500
    response = json.loads(response.data)
    assert response['msg'] == "Internal Server Error"


@pytest.mark.parametrize("uuid", [uuid4()])
def test_fetch_wager_random_uuid(uuid):
    response = app.test_client().get(f'/{uuid}')

    assert response.status_code == 404
    response = json.loads(response.data)
    assert response['msg'] == 'Not Found'
    assert response['data'] is None


def test_create_wager_empty():
    response = app.test_client().post('/', data={'data': '{}'},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['wager']['status_uuid'] == str(pytest.wagers[0].status_uuid)


def test_create_wager_w_members():
    members = [str(uuid4()), str(uuid4())]
    response = app.test_client().post('/', data={'data': json.dumps({'members': members})},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['wager']['status_uuid'] == str(pytest.wagers[0].status_uuid)
    assert response['data']['wager']['party_uuid'] is not None


def test_create_wager_w_stake():
    currency = "CAD"
    amount = "100"
    response = app.test_client().post('/', data={'data': json.dumps({'currency': currency, 'amount': amount})},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['wager']['status_uuid'] == str(pytest.wagers[0].status_uuid)
    assert response['data']['wager']['stake_uuid'] is not None


def test_create_wager_w_course():
    course = str(pytest.wagers[0].course_uuid)
    response = app.test_client().post('/', data={'data': json.dumps({'course': course})},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['wager']['status_uuid'] == str(pytest.wagers[0].status_uuid)
    assert response['data']['wager']['course_uuid'] is not None


def test_create_wager_w_time():
    time = common.utils.time_now() + 10000
    response = app.test_client().post('/', data={'data': json.dumps({'time': time})},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['wager']['status_uuid'] == str(pytest.wagers[0].status_uuid)
    assert response['data']['wager']['time'] == time
# def test_update_wager():
#     response = app.test_client().put('/', data={'data': '{}'},
#                                      headers={'X-Consumer-Custom-ID': '16ba5507-71b2-4fc9-8bbd-1909259c1ea1'})
#
#     assert response.status_code == 200
#     assert b'OK' in response.data

# def test_destroy_wager():
#     response = app.test_client().delete('/', data={'data': '{}'},
#                                         headers={'X-Consumer-Custom-ID': '16ba5507-71b2-4fc9-8bbd-1909259c1ea1'})
#
#     assert response.status_code == 200
#     assert b'OK' in response.data
