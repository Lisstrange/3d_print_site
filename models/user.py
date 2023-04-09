from db import BaseMeta
import ormar
from uuid import UUID, uuid4


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"

    id: UUID = ormar.UUID(
        primary_key=True,
        default=uuid4,
        uuid_format="string"
    )
    email: str = ormar.String(max_length=100, nullable=False, default="user@example.com")
    hashed_password: str = ormar.String(max_length=1000, nullable=False)
    given_name: str = ormar.String(max_length=100, default="Ivan")
    family_name: str = ormar.String(max_length=100, default="Ivanov")
    patronymic: str = ormar.String(max_length=100, default="Jovanovich")
    phone_number: str = ormar.String(max_length=11, min_length=11, default="88005553535")
    city: str = ormar.String(max_length=100, default="Your city")
    street: str = ormar.String(max_length=100, default="Your street")
    home: str = ormar.String(max_length=100, default="home number and building num")
    flat: str = ormar.Integer(default=0)
