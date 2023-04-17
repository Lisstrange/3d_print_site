from fastapi import APIRouter
from starlette.requests import Request
from starlette.templating import Jinja2Templates
import schemas
import security
from utils import settings
templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get('/')
def google_auth(request: Request):
    print(request)
    return templates.TemplateResponse("auth.html", {"request": request,
                                                    "GOOGLE_CLIENT_ID": settings.GOOGLE_CLIENT_ID,
                                                    "API_LOCATION": "http://127.0.0.1:8000",
                                                    "SWAP_TOKEN_ENDPOINT": "/swap_token",
                                                    "SUCCESS_ROUTE": "/users/me",
                                                    "ERROR_ROUTE": "/login_error"})


@router.post('/google/auth', response_model=schemas.Token)
async def google_auth(user: schemas.UserCreate):
    print(user)
    user_id, token = await security.google_auth(user)
    return schemas.Token(id=user_id, token=token)