from db import BaseMeta
import ormar
from uuid import UUID, uuid4


class Customer(ormar.Model):
    class Meta(BaseMeta):
        tablename = "customer"

    id: UUID = ormar.UUID(
        primary_key=True,
        default=uuid4,
        uuid_format="string"
    )
    first_name: str = ormar.String(max_length=100)
    last_name: str = ormar.String(max_length=100)
    surname: str = ormar.String(max_length=100)
    phone_number: str = ormar.String(max_length=11, min_length=11)
    city: str = ormar.String(max_length=100)
    street: str = ormar.String(max_length=100)
    home: str = ormar.String(max_length=100)
    flat: str = ormar.String(max_length=100)
