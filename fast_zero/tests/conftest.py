import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import User, table_registry


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def users(session):
    users = []
    for user_info in ['maria', 'joao', 'pedro', 'ana']:
        user = User(
            **{
                'username': user_info,
                'email': f'{user_info}@gmail.com',
                'password': f'{user_info}password',
            }
        )
        # user = User(
        # username='teste', email='test@gmail.com', password='senhateste123'
        # )

        session.add(user)
        session.commit()

        users.append(user)

    return users


@pytest.fixture()
def user(session):
    user = User(
        username='teste', email='test@gmail.com', password='senhateste123'
    )

    session.add(user)
    session.commit()

    return user


@pytest.fixture()
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
