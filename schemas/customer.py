from models import Customer
from pydantic import BaseModel
from uuid import UUID
from typing import Optional

CustomerBaseRequestSchema = Customer.get_pydantic(
    exclude={
        "id",
        "orders"
    }
)

CustomerBaseResponseSchema = Customer.get_pydantic()


class CustomerCreateRequestSchema(CustomerBaseRequestSchema):
    last_name: Optional[str] = ""
    surname: Optional[str] = ""
    city: Optional[str] = ""
    street: Optional[str] = ""
    home: Optional[str] = ""
    flat: Optional[int] = 0
