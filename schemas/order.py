from datetime import date
from pathlib import Path
from models import Order
from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from models.order import MaterialTypeEnum, DeliveryTypeEnum

OrderBaseRequestSchema = Order.get_pydantic(
    exclude={"id"}
)

OrderBaseResponseSchema = Order.get_pydantic()

OrderCreateRequestSchema = Order.get_pydantic(
    exclude={"id", "customer"}
)


class OrderUpdateRequestSchema(OrderBaseRequestSchema):
    order_date: Optional[date] = date.today()
    price: Optional[int] = 0
    material: Optional[MaterialTypeEnum] = MaterialTypeEnum.abc
    archive_path: Optional[Path] = Path.cwd()
    delivery_type: Optional[DeliveryTypeEnum] = DeliveryTypeEnum.sdek
