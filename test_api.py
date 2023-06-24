import requests
from jsonschema.validators import validate
from helper import load_json_schema, CustomSession, reqres_session


def test_list_users():
    response = reqres_session.get('/api/users?page=2')
    schema = load_json_schema('list_users.json')

    validate(instance=response.json(), schema=schema)

    assert response.status_code == 200, f'Ожидаемый статус код 200. Пришедший статус код {response.status_code}'
    assert response.json()['per_page'] == 6
    assert response.json()['total'] == 12


def test_single_user():
    response = reqres_session.get('/api/users/2')
    schema = load_json_schema('single_user.json')

    validate(instance=response.json(), schema=schema)

    assert response.status_code == 200, f'Ожидаемый статус код 200. Пришедший статус код {response.status_code}'
    assert response.json()['data']['id'] == 2
    assert response.json()['data']['email'] == 'janet.weaver@reqres.in'


def test_single_user_not_found():
    response = reqres_session.get('/api/users/23')
    schema = load_json_schema('single_user_not_found.json')

    validate(instance=response.json(), schema=schema)

    assert response.status_code == 404, f'Ожидаемый статус код 404. Пришедший статус код {response.status_code}'


def test_list_resource():
    response = reqres_session.get('/api/unknown')
    schema = load_json_schema('list_resource.json')

    validate(instance=response.json(), schema=schema)

    assert response.status_code == 200, f'Ожидаемый статус код 200. Пришедший статус код {response.status_code}'
    assert response.json()['per_page'] == 6
    assert response.json()['total'] == 12


def test_single_resource():
    response = reqres_session.get('/api/unknown/2')
    schema = load_json_schema('single_resource.json')

    validate(instance=response.json(), schema=schema)

    assert response.status_code == 200, f'Ожидаемый статус код 200. Пришедший статус код {response.status_code}'
    assert response.json()['data']['id'] == 2
    assert response.json()['data']['name'] == 'fuchsia rose'
    assert response.json()['data']['year'] == 2001


def test_single_resource_not_found():
    response = reqres_session.get(f'/api/unknown/23')
    schema = load_json_schema('single_resource_not_found.json')

    validate(instance=response.json(), schema=schema)

    assert response.status_code == 404, f'Ожидаемый статус код 404. Пришедший статус код {response.status_code}'


def test_create():
    payload = {"name": "Kristina",
               "job": "QA"}
    response = reqres_session.post('/api/users', json=payload)
    schema = load_json_schema('create_user.json')

    validate(instance=response.json(), schema=schema)

    assert response.status_code == 201, f'Ожидаемый статус код 201. Пришедший статус код {response.status_code}'
    assert response.json()['name'] == 'Kristina'
    assert response.json()['job'] == 'QA'


def test_update_put():
    payload = {"name": "morpheus",
               "job": "zion resident"}
    response = reqres_session.put('/api/users/2', json=payload)
    schema = load_json_schema('update_put.json')

    validate(instance=response.json(), schema=schema)

    assert response.status_code == 200, f'Ожидаемый статус код 201. Пришедший статус код {response.status_code}'
    assert response.json()['name'] == 'morpheus'
    assert response.json()['job'] == 'zion resident'


def test_update_patch():
    payload = {"name": "morpheus",
               "job": "zion resident"}
    response = reqres_session.patch('/api/users/2', json=payload)
    schema = load_json_schema('update_patch.json')

    validate(instance=response.json(), schema=schema)

    assert response.status_code == 200, f'Ожидаемый статус код 201. Пришедший статус код {response.status_code}'
    assert response.json()['name'] == 'morpheus'
    assert response.json()['job'] == 'zion resident'


def test_register_successfull():
    payload = {"email": "eve.holt@reqres.in",
               "password": "pistol"}
    response = reqres_session.post('/api/register', json=payload)
    schema = load_json_schema('register_successfull.json')

    validate(instance=response.json(), schema=schema)

    assert response.status_code == 200, f'Ожидаемый статус код 200. Пришедший статус код {response.status_code}'
    assert response.json()['id'] == 4
    assert response.json()['token'] == 'QpwL5tke4Pnpja7X4'


def test_register_unsuccessfull():
    payload = {"email": "sydney@fife"}
    response = reqres_session.post('/api/register', json=payload)
    schema = load_json_schema('register_unsuccessfull.json')

    validate(instance=response.json(), schema=schema)

    assert response.status_code == 400, f'Ожидаемый статус код 400. Пришедший статус код {response.status_code}'
    assert response.json()['error'] == 'Missing password'


def test_login_successfull():
    payload = {"email": "eve.holt@reqres.in",
               "password": "cityslicka"}
    response = reqres_session.post('/api/login', json=payload)
    schema = load_json_schema('login_successfull.json')

    validate(instance=response.json(), schema=schema)

    assert response.status_code == 200, f'Ожидаемый статус код 200. Пришедший статус код {response.status_code}'
    assert response.json()['token'] == 'QpwL5tke4Pnpja7X4'


def test_login_unsuccessfull():
    payload = {"email": "peter@klaven"}
    response = reqres_session.post('/api/login', json=payload)
    schema = load_json_schema('login_unsuccessfull.json')

    validate(instance=response.json(), schema=schema)

    assert response.status_code == 400, f'Ожидаемый статус код 400. Пришедший статус код {response.status_code}'
    assert response.json()['error'] == 'Missing password'


def test_delayed_response():
    response = reqres_session.get('/api/users?delay=3')
    schema = load_json_schema('delayed_response.json')

    validate(instance=response.json(), schema=schema)

    assert response.status_code == 200, f'Ожидаемый статус код 200. Пришедший статус код {response.status_code}'
    assert response.json()['per_page'] == 6
    assert response.json()['total'] == 12