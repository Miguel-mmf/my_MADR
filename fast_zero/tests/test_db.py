# import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from fast_zero.models import User, table_registry


# @pytest.mark.skip()
def test_create_user():
    engine = create_engine(
        # 'sqlite:///database.db',
        'sqlite:///:memory:'
    )

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        user = User(
            username='miguel',
            password='admin123-Atualizada2024',
            email='miguel@gmail.com',
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        result = session.scalar(select(User).where(User.username == 'miguel'))

    assert user.id == 1
    assert user.username == 'miguel'
    assert user.password == 'admin123-Atualizada2024'
    assert user.email == 'miguel@gmail.com'
    assert user.created_at is not None

    assert result.id == 1
    assert result.username == 'miguel'
    assert result.password == 'admin123-Atualizada2024'
    assert result.email == 'miguel@gmail.com'
    assert result.created_at is not None


def teste_create_user_v02(session):
    user = User(
        username='miguel',
        password='admin123-Atualizada2024',
        email='miguel@gmail.com',
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    result = session.scalar(select(User).where(User.username == 'miguel'))

    assert user.id == 1
    assert user.username == 'miguel'
    assert user.password == 'admin123-Atualizada2024'
    assert user.email == 'miguel@gmail.com'
    assert user.created_at is not None

    assert result.id == 1
    assert result.username == 'miguel'
    assert result.password == 'admin123-Atualizada2024'
    assert result.email == 'miguel@gmail.com'
    assert result.created_at is not None
