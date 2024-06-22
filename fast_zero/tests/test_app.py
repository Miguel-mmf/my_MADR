from http import HTTPStatus

import pytest

NUM_OF_USERS_CREATED = 4


def test_root_deve_retornar_ok_e_hello_user(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello, User!'}


def test_client_nao_deve_retornar_ok(client):
    response = client.get('/not_found')

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    'user',
    [
        {
            'username': user,
            'email': f'{user}@gmail.com',
            'password': f'{user}password',
        }
        for user in ['maria', 'joao', 'pedro', 'ana']
    ],
)
def test_create_user(client, user):
    response = client.post(
        '/user/',
        json=user,
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['username'] == user['username']
    assert response.json()['email'] == user['email']
    assert 'password' not in response.json()
    assert 'id' in response.json()


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert 'users' in response.json()
    assert len(response.json()['users']) == NUM_OF_USERS_CREATED
    assert response.json() == {
        'users': [
            {
                'id': id + 1,
                'username': user,
                'email': f'{user}@gmail.com',
            }
            for id, user in enumerate(['maria', 'joao', 'pedro', 'ana'])
        ],
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'user_updated',
            'email': 'user_updated@gmail.com',
            'password': 'password_updated',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'user_updated',
        'email': 'user_updated@gmail.com',
    }


def test_update_user_not_found(client):
    response = client.put(
        '/users/5',
        json={
            'username': 'user_updated',
            'email': 'user_update@gmail.com',
            'password': 'password_updated',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found.'}


def test_delete_user_not_found(client):
    response = client.delete('/users/5')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found.'}
    assert (
        len(client.get('/users/').json()['users'])
        == NUM_OF_USERS_CREATED
    )


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted.'}
    assert (
        len(client.get('/users/').json()['users']) == NUM_OF_USERS_CREATED - 1
    )

    assert client.get('/users/').json() == {
        'users': [
            {
                'id': id + 1,
                'username': user,
                'email': f'{user}@gmail.com',
            }
            for id, user in enumerate(['maria', 'joao', 'pedro', 'ana'])
            if id != 0
        ],
    }
