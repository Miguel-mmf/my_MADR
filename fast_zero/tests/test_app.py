from http import HTTPStatus


def test_root_deve_retornar_ok_e_hello_user(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello, User!'}


def test_client_nao_deve_retornar_ok(client):
    response = client.get('/not_found')

    assert response.status_code == HTTPStatus.NOT_FOUND
