from http import HTTPStatus

from fastapi import FastAPI, HTTPException

# pass as response_class to return HTML content
# from fastapi.responses import HTMLResponse
from fast_zero.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()

tmp_database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello, User!'}
    # return read_root_formatting_with_html()


@app.post('/user/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(id=len(tmp_database) + 1, **user.model_dump())
    tmp_database.append(user_with_id)

    return user_with_id


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
    return {'users': tmp_database}


@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(user_id: int, user: UserSchema):
    try:
        user_index = user_id - 1
        tmp_database[user_index] = UserDB(id=user_id, **user.model_dump())
    except IndexError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found.'
        )

    return tmp_database[user_index]


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(user_id: int):
    try:
        user_index = user_id - 1
        tmp_database.pop(user_index)
    except IndexError:
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
