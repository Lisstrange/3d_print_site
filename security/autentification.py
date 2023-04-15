from datetime import datetime, timedelta
from utils import settings
from authlib.jose import jwt
from uuid import UUID
access_token_jwt_subject = "access"


def create_token_by_id(user_id: UUID) -> dict:
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
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    # TODO поменять на правильную реализацию, ссылка на пример:  https://docs.authlib.org/en/latest/jose/jwt.html?highlight=jwt#json-web-token-jwt
    # header = {'alg': settings.ALGORITHM}
    # payload = to_encode
    # private_key =settings.SECRET_KEY
    # encoded_jwt = jwt.encode(header, payload, private_key)
    return encoded_jwt
