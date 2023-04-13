from datetime import datetime, timedelta
from utils import settings

access_token_jwt_subject = "access"


def create_token(user_id: int) -> dict:
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            data={"user_id": user_id}, expires_delta=access_token_expires
        ),
        "token_type": "Token"
    }


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=25)
    to_encode.update({"exp": expire,
                      "sub": access_token_jwt_subject})
    encoded_jwt = # TODO Написать через authlib jwt.encode()...  Время 41:01
