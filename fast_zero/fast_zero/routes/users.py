from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

# pass as response_class to return HTML content
# from fastapi.responses import HTMLResponse
from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import (
    FilterPage,
    Message,
    UserList,
    UserPublic,
    UserSchema,
)
from fast_zero.security import (
    get_current_user,
    get_password_hash,
)

router = APIRouter(
    prefix='/users',
    tags=['users'],
)

# tmp_database = []

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session):
    if db_user := session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    ):
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='User with this name already exists.',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status=HTTPStatus.BAD_REQUEST,
                detail='User with this email already exists.',
            )

    hashed_password = get_password_hash(user.password)

    db_user = User(
        username=user.username, password=hashed_password, email=user.email
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user
    # user_with_id = UserDB(id=len(tmp_database) + 1, **user.model_dump())
    # tmp_database.append(user_with_id)

    # return user_with_id


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    session: Session, filter_users: Annotated[FilterPage, Depends()]
):
    users = session.scalars(
        select(User).offset(filter_users.offset).limit(filter_users.limit)
    ).all()

    return {'users': users}


@router.put('/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session,
    current_user: CurrentUser,
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You do not have permission to update this user.',
        )

    # if not(db_user:= session.scalar(select(User).where(User.id == user_id))):
    #     raise HTTPException(
    #         status_code=HTTPStatus.NOT_FOUND, detail='User not found.'
    #     )

    try:
        current_user.username = user.username
        current_user.email = user.email
        current_user.password = get_password_hash(user.password)

        session.add(current_user)
        session.commit()
        session.refresh(current_user)
        return current_user
    except IntegrityError as e:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='User with this name or email already exists.',
        ) from e


@router.delete('/{user_id}', status_code=HTTPStatus.OK, response_model=Message)
def delete_user(
    user_id: int,
    session: Session,
    current_user: CurrentUser,
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You do not have permission to delete this user.',
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted.'}
