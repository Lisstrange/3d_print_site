from typing import List
from models import User
from fastapi.routing import APIRouter
import schemas
import models
from uuid import UUID
# from security.hasher import Hasher
router = APIRouter()


@router.get(
    "/",
    response_model=List[User]
)
async def get_all_users():
    return await User.objects.all()

#
# @router.post(
#     "/",
#     response_model=schemas.UserBaseResponseSchema
# )
# async def create_user(user: schemas.UserBaseRequestSchema):
#     user.hashed_password = Hasher.get_password_hash(user.hashed_password)
#     return await models.User.objects.create(**user.dict())
#

@router.get(
    "/{id}",
    response_model=schemas.UserBaseResponseSchema
)
async def get_user_by_id(pk: UUID) -> User:
    instance = await User.objects.get_or_none(id=pk)
    return instance


@router.patch(
    "/{id}",
    response_model=schemas.UserBaseResponseSchema
)
async def update_user_info(pk: UUID,
                               info: schemas.UserBaseRequestSchema):
    print(type(info))
    instance = await get_user_by_id(pk)
    return await instance.update(**info.dict(exclude={"id"},
                                             exclude_none=True,
                                             exclude_unset=True,
                                             exclude_defaults=True,
                                             exclude_relations=True
                                             ))


@router.delete("/{id}")
async def delete_user(pk: UUID):
    instance = await get_user_by_id(pk)
    deleted_records = await instance.delete()
    return None





from datetime import datetime, timedelta
from typing import Annotated

# from security.hasher import Hasher
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from models import User
from utils import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token", auto_error=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


async def get_user_by_email(email: str) -> User:
    instance = await User.objects.get_or_none(email=email)
    return instance


# async def authenticate_user(email: str, password) -> User | None:
#     user = await get_user_by_email(email)
#     if not user:
#         return None
#     if not Hasher.verify_password(password, user.hashed_password):
#         return None
#     return user
#
#
# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
#     return encoded_jwt
#
#
# async def get_current_user_from_token(token: Annotated[str, Depends(oauth2_scheme)]) -> User | None:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",) # TODO - прокинуть этот exception в exceptions
#     try:
#         payload = jwt.decode(
#             token, settings.SECRET_KEY,
#             algorithms=settings.ALGORITHM
#         )
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except Exception as e:
#         raise credentials_exception
#     user = get_user_by_email(username=token_data.username)
#
#     if user is None:
#         raise credentials_exception
#     return user
#
# # TODO - https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#handle-jwt-tokens
#
# # @router.post("/token", response_model=Token)
#
#
# @router.get("/")
# async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {"token": token}
