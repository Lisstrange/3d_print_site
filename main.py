import uvicorn
from fastapi import FastAPI
from utils import settings
import api
from api.endpoints.auth import router
from db import BaseMeta
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI(
    title="3d_ded", docs_url=None, redoc_url=None
)
app.include_router(api.router)
app.include_router(router)
app.state.database = BaseMeta.database

app.add_middleware(SessionMiddleware, secret_key='!secret')


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

from authlib.integrations.starlette_client import OAuth

# Initialize our OAuth instance from the client ID and client secret specified in our .env file

@app.get('/')
async def home(request: Request):
    # Try to get the user
    user = request.session.get('user')
    if user is not None:
        email = user['email']
        html = (
            f'<pre>Email: {email}</pre><br>'
            '<a href="/docs">documentation</a><br>'
            '<a href="/logout">logout</a>'
        )
        return HTMLResponse(html)

    # Show the login link
    return HTMLResponse('<a href="/login">login</a>')

# --- Google OAuth ---

# Initialize our OAuth instance from the client ID and client secret specified in our .env file
config = Config('.env')
oauth = OAuth(config)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)
#
# oauth.register(
#     name="google",
#     client_id=settings.GOOGLE_CLIENT_ID,
#     client_secret=settings.CLIENT_SECRET,
#     authorize_url="https://accounts.google.com/o/oauth2/auth",
#     access_token_url="https://accounts.google.com/o/oauth2/token",
#     api_base_url="https://www.googleapis.com/",
#     client_kwargs={"scope": "nikita.a.lisovik@gmail.com"},
#     server_metadata_url=CONF_URL,
# )

@app.get('/login', tags=['authentication'])  # Tag it as "authentication" for our docs
async def login(request: Request):
    # Redirect Google OAuth back to our application
    redirect_uri = request.url_for('auth')

    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.route('/auth')
async def auth(request: Request):
    # Perform Google OAuth
    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)

    # Save the user
    request.session['user'] = dict(user)

    return RedirectResponse(url='/')


@app.get('/logout', tags=['authentication'])  # Tag it as "authentication" for our docs
async def logout(request: Request):
    # Remove the user
    request.session.pop('user', None)

    return RedirectResponse(url='/')


# --- Dependencies ---


# Try to get the logged in user
async def get_user(request: Request) -> Optional[dict]:
    user = request.session.get('user')
    if user is not None:
        return user
    else:
        raise HTTPException(status_code=403, detail='Could not validate credentials.')

    return None


# --- Documentation ---


@app.route('/openapi.json')
async def get_open_api_endpoint(request: Request, user: Optional[dict] = Depends(get_user)):  # This dependency protects our endpoint!
    response = JSONResponse(get_openapi(title='FastAPI', version=1, routes=app.routes))
    return response


@app.get('/docs', tags=['documentation'])  # Tag it as "documentation" for our docs
async def get_documentation(request: Request, user: Optional[dict] = Depends(get_user)):  # This dependency protects our endpoint!
    response = get_swagger_ui_html(openapi_url='/openapi.json', title='Documentation')
    return response


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True
    )
