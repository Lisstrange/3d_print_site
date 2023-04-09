from passlib.context import CryptContext

pwd_context = CryptContext(
    schemas=["bcrypt", "sha256_crypt"],
    bcrypt__default_rounds=1337,
    sha256_crypt__default_rounds=322,
)


class PasswordHasher:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        return pwd_context.verify(password, password_hash)





from fastapi import FastAPI, HTTPException
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Optional
import ormar
import databases


app = FastAPI()

# Создаем объект для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Создаем базу данных и модель пользователя
DATABASE_URL = "sqlite:///./test.db"
database = databases.Database(DATABASE_URL)

class User(ormar.Model):
    class Meta:
        tablename = "users"
        database = database

    id: int = ormar.Integer(primary_key=True)
    email: str = ormar.String(max_length=100, unique=True)
    hashed_password: str = ormar.String(max_length=100)


# Создаем таблицу пользователей при запуске приложения
@app.on_event("startup")
async def startup():
    await database.connect()
    await User.create_table()


# Создаем модель для запроса на создание пользователя
class CreateUserRequest(BaseModel):
    email: str
    password: str


# Создаем модель для ответа при успешном создании пользователя
class CreateUserResponse(BaseModel):
    email: str


# Создаем эндпоинт для создания пользователя
@app.post("/users", response_model=CreateUserResponse)
async def create_user(user: CreateUserRequest):
    # Хешируем пароль с использованием соли
    hashed_password = pwd_context.hash(user.password + "random_salt")
    # Создаем нового пользователя в базе данных
    new_user = await User(email=user.email, hashed_password=hashed_password).save()
    return CreateUserResponse(email=new_user.email)


# Создаем модель для запроса на аутентификацию пользователя
class AuthenticateUserRequest(BaseModel):
    email: str
    password: str


# Создаем модель для ответа при успешной аутентификации пользователя
class AuthenticateUserResponse(BaseModel):
    email: str


# Создаем эндпоинт для аутентификации пользователя
@app.post("/auth", response_model=AuthenticateUserResponse)
async def authenticate_user(user: AuthenticateUserRequest):
    # Получаем пользователя из базы данных по email
    db_user = await User.objects.get_or_none(email=user.email)
    # Если пользователь не найден, возвращаем ошибку
    if db_user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    # Проверяем пароль на соответствие хешу
    if not pwd_context.verify(user.password + "random_salt", db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return AuthenticateUserResponse(email=db_user.email)