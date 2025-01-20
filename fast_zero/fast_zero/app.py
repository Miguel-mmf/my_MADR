from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

# pass as response_class to return HTML content
# from fastapi.responses import HTMLResponse
from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, Token, UserList, UserPublic, UserSchema
from fast_zero.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)

app = FastAPI(
    title='My MADR API with FastAPI',
    description='A simple API to manage users.',
    version='0.1.0',
)

tmp_database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello, User!'}
    # return read_root_formatting_with_html()


@app.post('/token/', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect username or password.',
        )

    access_token = create_access_token(data={'sub': user.email})
    return {'access_token': access_token, 'token_type': 'bearer'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
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


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    limit: int = 10, offset: int = 0, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(offset).limit(limit)).all()

    return {'users': users}


@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
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


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You do not have permission to delete this user.',
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted.'}


def read_root_formatting_with_html():
    """
    Returns a formatted HTML string with a title and a greeting message.

    Returns:
        str: HTML content with a title and a greeting message.
    """

    return """
    <html>
        <head>
            <title>Fast Zero</title>
        </head>
        <body>
            <h1>Hello, User!</h1>
        </body>
    </html>
    """
