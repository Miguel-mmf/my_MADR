from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_root_deve_retornar_ok_e_hello_user():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello, User!'}


def test_client_nao_deve_retornar_ok():
    client = TestClient(app)

    response = client.get("/not_found")

    assert response.status_code == HTTPStatus.NOT_FOUND
