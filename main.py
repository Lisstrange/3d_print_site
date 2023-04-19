import uvicorn
from fastapi import FastAPI
from utils import settings
import api
from api.endpoints.auth import router
from db import BaseMeta
from starlette.middleware.sessions import SessionMiddleware
import os
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(
    title="3d_ded", docs_url=None, redoc_url=None
)
app.include_router(api.router)
app.include_router(router)
app.state.database = BaseMeta.database

SECRET_KEY = os.environ.get("SECRET_KEY")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


from fastapi import APIRouter
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()

from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from starlette.config import Config
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse

from authlib.integrations.starlette_client import OAuth, OAuthError

# Initialize our OAuth instance from the client ID and client secret specified in our .env file

import json


@app.get('/')
async def home(request: Request):
    # Try to get the user
    user = request.session.get('user')
    if user:
        data = json.dumps(user)
        html = (
            f'<pre>{data}</pre>'
            '<a href="/logout">logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="/login">login</a>')


# --- Google OAuth ---

# Initialize our OAuth instance from the client ID and client secret specified in our .env file
config = Config('.env')
oauth = OAuth(config)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name="google",
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

from pprint import pprint


@app.get('/login', tags=['authentication'])  # Tag it as "authentication" for our docs
async def login(request: Request):
    # Redirect Google OAuth back to our application
    redirect_uri = request.url_for('auth').__str__()
    pprint(request.__dict__)
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.get('/auth')
async def auth(request: Request):
    print("START AUTH")
    try:
        pprint(request.__dict__)
        token = await oauth.google.authorize_access_token(request)
        pprint(token)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse(url='/')


@app.get('/logout', tags=['authentication'])  # Tag it as "authentication" for our docs
async def logout(request: Request):
    # Remove the user
    request.session.pop('user', None)

    return RedirectResponse(url='/')


# --- Dependencies ---


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True
    )
