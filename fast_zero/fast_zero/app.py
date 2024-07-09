from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

# pass as response_class to return HTML content
# from fastapi.responses import HTMLResponse
from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, UserList, UserPublic, UserSchema

app = FastAPI()

tmp_database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello, User!'}
    # return read_root_formatting_with_html()


@app.post('/users', status_code=HTTPStatus.CREATED, response_model=UserPublic)
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

    db_user = User(
        username=user.username, password=user.password, email=user.email
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user
    # user_with_id = UserDB(id=len(tmp_database) + 1, **user.model_dump())
    # tmp_database.append(user_with_id)

    # return user_with_id


@app.get('/users', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    limit: int = 10, offset: int = 0, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(offset).limit(limit)).all()

    return {'users': users}


@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    if db_user := session.scalar(select(User).where(User.id == user_id)):
        db_user.username = user.username
        db_user.email = user.email
        db_user.password = user.password

        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found.'
        )

    return db_user


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    if db_user := session.scalar(select(User).where(User.id == user_id)):
        session.delete(db_user)
        session.commit()
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found.'
        )

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
