# import google.auth
# from google.oauth2.credentials import Credentials
#
# # Замените это значение своим идентификатором клиента OAuth2
# CLIENT_ID = '237999433766-h58j1hpl1gd79qvseiekh5qnkn217blf.apps.googleusercontent.com'
#
# # Замените это значение своим секретным ключом клиента OAuth2
# CLIENT_SECRET = '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'
#
# # Замените это значение своим URL-адресом перенаправления
# REDIRECT_URI = 'http://127.0.0.1:8000/api/v1/auth/'
#
# # Замените это значение на список требуемых областей доступа
# SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']
#
# # Получите авторизационный код от пользователя
# auth_url, _ = Credentials.from_client_info(
#     client_id=CLIENT_ID, client_secret=CLIENT_SECRET).authorization_url(
#         redirect_uri=REDIRECT_URI, scope=SCOPES)
# print('Перейдите по ссылке для авторизации: {}'.format(auth_url))
# auth_code = input('Введите авторизационный код: ')
#
# # Получите токен доступа OAuth2
# creds = Credentials.from_client_info(
#     client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
# creds.token = None
# creds.refresh_token = None
# creds.authorization_response = auth_code
# creds.refresh(google.auth.transport.requests.Request())
# print('Токен доступа: {}'.format(creds.token))
import requests
from fastapi import APIRouter

import models
import schemas

router = APIRouter()

from google.oauth2 import id_token
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from utils import settings
from fastapi import HTTPException
from models import User

async def create_user(user: schemas.UserCreate) -> User:
    instance = await models.User.objects.get_or_create(**user.dict())
    return instance

@router.post('/google',
             response_model=schemas.Token)
async def google_auth(user: schemas.UserCreate):
    try:
        idinfo = id_token.verify_oauth2_token(user.token, requests.Request(), settings.GOOGLE_CLIENT_ID)
    except ValueError:
        raise HTTPException(403, "Bad code")
    user = await create_user(user)
    print(user)
    return None
