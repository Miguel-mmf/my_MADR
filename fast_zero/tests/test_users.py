from http import HTTPStatus

import pytest

from fast_zero.schemas import UserPublic

NUM_OF_USERS_CREATED = 4


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
        '/users',
        json=user,
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['username'] == user['username']
    assert response.json()['email'] == user['email']
    assert 'password' not in response.json()
    assert 'id' in response.json()


def test_read_users(client):
    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK
    assert 'users' in response.json()
    assert response.json() == {'users': []}


def test_read_users_using_users_fixture(client, users):
    response = client.get('/users')

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


def test_read_users_using_user_fixture(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert 'users' in response.json()
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'user_updated',
            'email': 'user_updated@gmail.com',
            'password': 'password_updated',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': 'user_updated',
        'email': 'user_updated@gmail.com',
    }


def test_update_user_not_found(client, user, token):
    response = client.put(
        f'/users/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'user_updated',
            'email': 'user_update@gmail.com',
            'password': 'password_updated',
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': 'You do not have permission to update this user.'
    }


def test_update_user_with_wrong_user(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': 'You do not have permission to update this user.'
    }


def test_update_integrity_error(client, user, token):
    # Criando um registro para "fausto"
    client.post(
        '/users/',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    # Alterando o user.username das fixture para fausto
    response_update = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'fausto',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'User with this name or email already exists.'
    }


def test_delete_user_not_found(client, token):
    response = client.delete(
        '/users/5',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': 'You do not have permission to delete this user.'
    }


def test_delete_user_wrong_user(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': 'You do not have permission to delete this user.'
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted.'}
