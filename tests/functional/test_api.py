import json
import pytest
from uuid import uuid4
from src import app, services, common

# pytest --disable-pytest-warnings -s

pytest.wagers = services.find_wager()


def test_ping():
    response = app.test_client().get('/ping')

    assert response.status_code == 200
    assert b'pong' in response.data


# fetch all
def test_fetch_all_wager():
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert b'OK' in response.data


def test_fetch_all_wager_paginate():
    response = app.test_client().get('/?page=1&per_page=10')

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == 'OK'
    assert response['data']['_metadata']['total'] == 5
    assert response['data']['_metadata']['page'] == 1
    assert response['data']['_metadata']['per_page'] == 10
    assert len(response['data']['wager']) > 0

    response = app.test_client().get('/?page=2&per_page=10')

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == 'OK'
    assert response['data']['_metadata']['total'] == 5
    assert response['data']['_metadata']['page'] == 2
    assert response['data']['_metadata']['per_page'] == 10
    assert len(response['data']['wager']) == 0


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


@pytest.mark.parametrize("uuid", [uuid4()])
def test_fetch_wager_random_uuid(uuid):
    response = app.test_client().get(f'/{uuid}')

    assert response.status_code == 404
    response = json.loads(response.data)
    assert response['data'] == False
    assert response['msg'] == 'Not Found'

# def test_create_wager():
#     response = app.test_client().post('/', data={'data': '{}'},
#                                       headers={'X-Consumer-Custom-ID': '16ba5507-71b2-4fc9-8bbd-1909259c1ea1'})
#
#     assert response.status_code == 200
#     assert b'OK' in response.data

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
