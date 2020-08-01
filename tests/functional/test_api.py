import json
import pytest
from uuid import uuid4
from datetime import datetime
from src import app, services, common

# pytest --disable-pytest-warnings -s

pytest.wagers = services.find_wager()
pytest.owner = uuid4()
pytest.course = services.find_course_by_golf_canada_id(golf_canada_id=19679)  # northlands


def test_ping():
    response = app.test_client().get('/ping')

    assert response.status_code == 200
    assert b'pong' in response.data


# fetch all
def test_fetch_all_wager():
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert b'OK' in response.data


def test_fetch_all_wager_w_paginate_0():
    response = app.test_client().get('/?page=1&per_page=10')

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == 'OK'
    assert response['data']['_metadata']['total'] == 5
    assert response['data']['_metadata']['page'] == 1
    assert response['data']['_metadata']['per_page'] == 10
    assert len(response['data']['wager']) > 0


def test_fetch_all_wager_w_paginate_1():
    response = app.test_client().get('/?page=2&per_page=10')

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == 'OK'
    assert response['data']['_metadata']['total'] == 5
    assert response['data']['_metadata']['page'] == 2
    assert response['data']['_metadata']['per_page'] == 10
    assert len(response['data']['wager']) == 0


def test_fetch_all_wager_w_paginate_invalid_0():
    response = app.test_client().get('/?page=a&per_page=b')

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['data'] is None
    assert response['err']['page'][0] == "Not a valid integer."
    assert response['err']['per_page'][0] == "Not a valid integer."


def test_fetch_all_wager_w_paginate_invalid_1():
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
def test_fetch_wager_w_invalid_type(uuid):
    response = app.test_client().get(f'/{uuid}')

    assert response.status_code == 500
    response = json.loads(response.data)
    assert response['msg'] == "Internal Server Error"


@pytest.mark.parametrize("uuid", [uuid4()])
def test_fetch_wager_w_random_uuid(uuid):
    response = app.test_client().get(f'/{uuid}')

    assert response.status_code == 404
    response = json.loads(response.data)
    assert response['msg'] == 'Not Found'
    assert response['data'] is None


def test_create_wager_w_data_empty():
    response = app.test_client().post('/', json={},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['wager']['status_uuid'] == str(pytest.wagers[0].status_uuid)


def test_create_wager_w_opponents():
    opponents = [str(uuid4())]
    response = app.test_client().post('/', json={'opponents': opponents},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['wager']['status_uuid'] == str(pytest.wagers[0].status_uuid)
    assert response['data']['wager']['party_uuid'] is not None


def test_create_wager_w_stake_0():
    currency = "CAD"
    amount = "100"
    response = app.test_client().post('/', json={'currency': currency, 'amount': amount},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['wager']['status_uuid'] == str(pytest.wagers[0].status_uuid)
    assert response['data']['wager']['stake_uuid'] is not None


def test_create_wager_w_stake_0():
    currency = "CAD"
    amount = "99.99"
    response = app.test_client().post('/', json={'currency': currency, 'amount': amount},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['wager']['status_uuid'] == str(pytest.wagers[0].status_uuid)
    assert response['data']['wager']['stake_uuid'] is not None


def test_create_wager_w_stake_missing_currency():
    amount = "100"
    response = app.test_client().post('/', json={'amount': amount},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['wager']['stake_uuid'] is not None


def test_create_wager_w_stake_missing_amount():
    currency = "CAD"
    response = app.test_client().post('/', json={'currency': currency},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['wager']['stake_uuid'] is not None


def test_create_wager_w_course():
    course = str(pytest.wagers[0].course_uuid)
    response = app.test_client().post('/', json={'course': course},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['wager']['status_uuid'] == str(pytest.wagers[0].status_uuid)
    assert response['data']['wager']['course_uuid'] is not None


def test_create_wager_w_time():
    time = common.utils.time_now() + 10000
    response = app.test_client().post('/', json={'time': time},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['wager']['status_uuid'] == str(pytest.wagers[0].status_uuid)
    assert response['data']['wager']['time'] == time


def test_create_wager_wo_header():
    response = app.test_client().post('/', json={})

    assert response.status_code == 401
    response = json.loads(response.data)
    assert response['msg'] == "Unauthorized"


def test_create_wager_wo_json():
    response = app.test_client().post('/', json={}, headers={'X-Consumer-Custom-ID': '12345'})

    assert response.status_code == 401
    response = json.loads(response.data)
    assert response['msg'] == "Unauthorized"


def test_create_wager_w_opponents_invalid_type_0():
    opponents = ["dallanbhatti"]
    response = app.test_client().post('/', json={'opponents': opponents},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['err']['opponents']['0'][0] == "Not a valid UUID."


def test_create_wager_w_opponents_invalid_type_1():
    opponents = str(uuid4())
    response = app.test_client().post('/', json={'opponents': opponents},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['err']['opponents'][0] == "Not a valid list."


def test_create_wager_w_opponents_invalid_count_0():
    opponents = [str(uuid4()) for _ in range(2)]
    response = app.test_client().post('/', json={'opponents': opponents},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['err']['opponents'][0] == "Length must be 1."


def test_create_wager_w_opponents_invalid_count_1():
    opponents = [str(uuid4()) for _ in range(0)]
    response = app.test_client().post('/', json={'opponents': opponents},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['err']['opponents'][0] == "Length must be 1."


def test_create_wager_w_opponents_invalid_duplicate():
    opponent = str(uuid4())
    opponents = [opponent for _ in range(2)]
    response = app.test_client().post('/', json={'opponents': opponents},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['err']['opponents'][0] == "Length must be 1."


def test_create_wager_w_opponents_invalid_owner():
    opponents = [str(pytest.owner)]
    response = app.test_client().post('/', json={'opponents': opponents},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['err']['opponents'][0] == "Invalid value."


def test_create_wager_w_stake_currency_invalid_type():
    currency = 100
    amount = "100"
    response = app.test_client().post('/', json={'currency': currency, 'amount': amount},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['err']['currency'][0] == "Not a valid string."


def test_create_wager_w_stake_currency_invalid_value_0():
    currency = "CA"
    amount = "100"
    response = app.test_client().post('/', json={'currency': currency, 'amount': amount},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['err']['currency'][0] == "Invalid value."


def test_create_wager_w_stake_currency_invalid_value_1():
    currency = "$"
    amount = "100"
    response = app.test_client().post('/', json={'currency': currency, 'amount': amount},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['err']['currency'][0] == "Invalid value."


def test_create_wager_w_stake_amount_invalid_type():
    currency = "CAD"
    amount = "CAD"
    response = app.test_client().post('/', json={'currency': currency, 'amount': amount},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['err']['amount'][0] == "Not a valid number."


def test_create_wager_w_stake_amount_invalid_value_0():
    currency = "CAD"
    amount = "-1"
    response = app.test_client().post('/', json={'currency': currency, 'amount': amount},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})
    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['err']['amount'][0] == "Cannot be a negative value."


def test_create_wager_w_stake_amount_invalid_value_1():
    currency = "CAD"
    amount = "$100"
    response = app.test_client().post('/', json={'currency': currency, 'amount': amount},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['err']['amount'][0] == "Not a valid number."


def test_create_wager_w_course_invalid_type():
    course = 123
    response = app.test_client().post('/', json={'course': course},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['err']['course'][0] == "Not a valid UUID."


def test_create_wager_w_course_invalid_value():
    course = str(uuid4())
    response = app.test_client().post('/', json={'course': course},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['err']['course'][0] == "Invalid UUID."


def test_create_wager_w_time_invalid_type():
    time = str(datetime.now())
    response = app.test_client().post('/', json={'time': time},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['err']['time'][0] == "Not a valid integer."


def test_create_wager_w_time_invalid_value_0():
    time = common.utils.time_now() - 100000

    response = app.test_client().post('/', json={'time': time},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['err']['time'][0] == "Must be greater than current time."


def test_create_wager_w_time_invalid_value_1():
    time = common.utils.add_years(common.utils.time_now(), 2)

    response = app.test_client().post('/', json={'time': time},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['err']['time'][0] == "Must be within the next year."


def test_create_wager_w_invalid_data():
    money = "50"

    response = app.test_client().post('/', json={'money': money},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['err']['money'][0] == "Unknown field."


def test_create_wager_w_duplicate_data():
    time = common.time_now() + 10000
    course = pytest.wagers[0].course_uuid
    currency = "CAD"
    amount = "100"
    opponents = [str(uuid4())]

    response = app.test_client().post('/', json={'time': time, 'course': course, 'currency': currency, 'amount': amount,
                                                 'opponents': opponents},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"

    response = app.test_client().post('/', json={'time': time, 'course': course, 'currency': currency, 'amount': amount,
                                                 'opponents': opponents},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"


def test_update_wager_w_time():
    uuid = pytest.wagers[0].uuid
    time = common.time_now() + 50000
    owner = pytest.wagers[0].owner
    response = app.test_client().put(f'/{uuid}',
                                     json={'time': time},
                                     headers={'X-Consumer-Custom-ID': owner})

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"


def test_update_wager_w_course():
    uuid = pytest.wagers[0].uuid
    course = str(pytest.course.uuid)
    owner = pytest.wagers[0].owner
    response = app.test_client().put(f'/{uuid}',
                                     json={'course': course},
                                     headers={'X-Consumer-Custom-ID': owner})

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"


def test_update_wager_w_stake_currency():
    uuid = pytest.wagers[0].uuid
    currency = "USD"
    owner = pytest.wagers[0].owner
    response = app.test_client().put(f'/{uuid}',
                                     json={'currency': currency},
                                     headers={'X-Consumer-Custom-ID': owner})

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"


def test_update_wager_w_stake_amount():
    uuid = pytest.wagers[0].uuid
    amount = "5000"
    owner = pytest.wagers[0].owner
    response = app.test_client().put(f'/{uuid}',
                                     json={'amount': amount},
                                     headers={'X-Consumer-Custom-ID': owner})

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"


def test_update_wager_w_opponents():
    time = common.time_now()
    response = app.test_client().post('/', json={'time': time},
                                      headers={'X-Consumer-Custom-ID': pytest.owner})
    assert response.status_code == 200
    response = json.loads(response.data)
    uuid = response['data']['wager']['uuid']
    opponents = [uuid4()]
    response = app.test_client().put(f'/{uuid}',
                                     json={'opponents': opponents},
                                     headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"


def test_update_wager_wo_data():
    uuid = pytest.wagers[0].uuid
    owner = pytest.wagers[0].owner
    response = app.test_client().put(f'/{uuid}',
                                     json={},
                                     headers={'X-Consumer-Custom-ID': owner})

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"


def test_update_wager_wo_header():
    uuid = pytest.wagers[0].uuid
    amount = "5000"
    response = app.test_client().put(f'/{uuid}', json={'amount': amount})

    assert response.status_code == 401
    response = json.loads(response.data)
    assert response['msg'] == "Unauthorized"


def test_update_wager_w_uuid_invalid_data():
    uuid = uuid4()
    amount = "5000"
    owner = pytest.wagers[0].owner
    response = app.test_client().put(f'/{uuid}',
                                     json={'amount': amount},
                                     headers={'X-Consumer-Custom-ID': owner})

    assert response.status_code == 404
    response = json.loads(response.data)
    assert response['msg'] == "Not Found"


def test_update_wager_w_owner_invalid_data():
    uuid = pytest.wagers[0].uuid
    amount = "5000"
    owner = uuid4()
    response = app.test_client().put(f'/{uuid}',
                                     json={'amount': amount},
                                     headers={'X-Consumer-Custom-ID': owner})
    assert response.status_code == 403
    response = json.loads(response.data)
    assert response['msg'] == "Forbidden"
    assert response['err']['wager'][0] == "Update is only available to owner"


def test_update_wager_w_opponents_invalid_value():
    uuid = pytest.wagers[0].uuid
    owner = pytest.wagers[0].owner
    opponents = [str(uuid4())]
    response = app.test_client().put(f'/{uuid}', json={'opponents': opponents},
                                     headers={'X-Consumer-Custom-ID': owner})

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"


def test_update_wager_w_stake_currency_invalid_type():
    uuid = pytest.wagers[0].uuid
    currency = 100
    amount = "100"
    response = app.test_client().put(f'/{uuid}', json={'currency': currency, 'amount': amount},
                                     headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['err']['currency'][0] == "Not a valid string."


def test_update_wager_w_stake_currency_invalid_value_0():
    uuid = pytest.wagers[0].uuid
    currency = "CA"
    amount = "100"
    response = app.test_client().put(f'/{uuid}', json={'currency': currency, 'amount': amount},
                                     headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['err']['currency'][0] == "Invalid value."


def test_update_wager_w_stake_currency_invalid_value_1():
    uuid = pytest.wagers[0].uuid
    currency = "$"
    amount = "100"
    response = app.test_client().put(f'/{uuid}', json={'currency': currency, 'amount': amount},
                                     headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['err']['currency'][0] == "Invalid value."


def test_update_wager_w_stake_amount_invalid_type():
    uuid = pytest.wagers[0].uuid
    currency = "CAD"
    amount = "CAD"
    response = app.test_client().put(f'/{uuid}', json={'currency': currency, 'amount': amount},
                                     headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['err']['amount'][0] == "Not a valid number."


def test_update_wager_w_stake_amount_invalid_value_0():
    uuid = pytest.wagers[0].uuid
    currency = "CAD"
    amount = "-1"
    response = app.test_client().put(f'/{uuid}', json={'currency': currency, 'amount': amount},
                                     headers={'X-Consumer-Custom-ID': pytest.owner})
    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['err']['amount'][0] == "Cannot be a negative value."


def test_update_wager_w_stake_amount_invalid_value_1():
    uuid = pytest.wagers[0].uuid
    currency = "CAD"
    amount = "$100"
    response = app.test_client().put(f'/{uuid}', json={'currency': currency, 'amount': amount},
                                     headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['err']['amount'][0] == "Not a valid number."


def test_update_wager_w_course_invalid_type():
    uuid = pytest.wagers[0].uuid
    course = 123
    response = app.test_client().put(f'/{uuid}', json={'course': course},
                                     headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['err']['course'][0] == "Not a valid UUID."


def test_update_wager_w_course_invalid_value():
    uuid = pytest.wagers[0].uuid
    owner = pytest.wagers[0].owner
    course = str(uuid4())
    response = app.test_client().put(f'/{uuid}', json={'course': course},
                                     headers={'X-Consumer-Custom-ID': owner})

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['err']['course'][0] == "Invalid UUID."


def test_update_wager_w_time_invalid_type():
    uuid = pytest.wagers[0].uuid
    time = str(datetime.now())
    response = app.test_client().put(f'/{uuid}', json={'time': time},
                                     headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['err']['time'][0] == "Not a valid integer."


def test_update_wager_w_time_invalid_value_0():
    uuid = pytest.wagers[0].uuid
    time = common.utils.time_now() - 100000

    response = app.test_client().put(f'/{uuid}', json={'time': time},
                                     headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['err']['time'][0] == "Must be greater than current time."


def test_update_wager_w_time_invalid_value_1():
    uuid = pytest.wagers[0].uuid
    time = common.utils.add_years(common.utils.time_now(), 2)

    response = app.test_client().put(f'/{uuid}', json={'time': time},
                                     headers={'X-Consumer-Custom-ID': pytest.owner})

    assert response.status_code == 400
    response = json.loads(response.data)
    assert response['msg'] == "Bad Request"
    assert response['err']['time'][0] == "Must be within the next year."

# def test_destroy_wager():
#     response = app.test_client().delete('/', data={'data': '{}'},
#                                         headers={'X-Consumer-Custom-ID': '16ba5507-71b2-4fc9-8bbd-1909259c1ea1'})
#
#     assert response.status_code == 200
#     assert b'OK' in response.data
