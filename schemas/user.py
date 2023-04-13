from models import User
from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional

UserBaseRequestSchema = User.get_pydantic(
    exclude={
        "id",
        "orders"
    }
)

UserBaseResponseSchema = User.get_pydantic()


class User(BaseModel):
    username: str
    email: EmailStr
    avatar: str


class UserCreate(User):
    token: str
class Token(BaseModel):
    id: int
    token: str


class UserUpdateRequestSchema(UserBaseRequestSchema):
    family_name: Optional[str] = ""
    patronymic: Optional[str] = ""
    city: Optional[str] = ""
    street: Optional[str] = ""
    home: Optional[str] = ""
    flat: Optional[int] = 0
