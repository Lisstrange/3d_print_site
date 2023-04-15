from fastapi import APIRouter
from starlette.requests import Request
from starlette.templating import Jinja2Templates
import schemas
import security
from utils import settings
templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get('/google')
async def google_auth(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request,
                                                    "GOOGLE_CLIENT_ID": settings.GOOGLE_CLIENT_ID})


@router.post('/google/auth', response_model=schemas.Token)
async def google_auth(user: schemas.UserCreate):
    user_id, token = await security.google_auth(user)
    return schemas.Token(id=user_id, token=token)