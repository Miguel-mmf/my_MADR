from http import HTTPStatus

from fastapi import FastAPI

# pass as response_class to return HTML content
# from fastapi.responses import HTMLResponse
from fast_zero.routes import auth, users
from fast_zero.schemas import Message

app = FastAPI(
    title='My MADR API with FastAPI',
    description='A simple API to manage users.',
    version='0.1.0',
)

app.include_router(users.router)
app.include_router(auth.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello, User!'}
    # return read_root_formatting_with_html()


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
