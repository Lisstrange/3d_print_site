from datetime import datetime
from enum import Enum
import ormar
from db import BaseMeta
from uuid import UUID, uuid4
from .user import User


class DeliveryTypeEnum(Enum):
    sdek = "Сдэк"
    pochta_rossii = "Почта России"
    boxberry = "Боксбери"
    samovivoz = "Самовывоз"

class MaterialTypeEnum(Enum):
    petg = "PETG"
    abc = "ABC"
    pla = "PLA"
    others = "Остальные типы пластиков"


class Order(ormar.Model):
    class Meta(BaseMeta):
        tablename = "orders"

    id: UUID = ormar.UUID(primary_key=True,
                          uuid_format="string",
                          default=uuid4)
    user: UUID = ormar.ForeignKey(User)
    order_date: datetime.date = ormar.DateTime(default=datetime.now())
    price: int = ormar.Integer(default=0)
    material: MaterialTypeEnum = ormar.String(max_length=100,
                                              choices=MaterialTypeEnum,
                                              default=MaterialTypeEnum.abc)
    archive_path: str = ormar.String(max_length=100)
    delivery_type: DeliveryTypeEnum = ormar.String(max_length=100,
                                                   choices=DeliveryTypeEnum,
                                                   default=DeliveryTypeEnum.sdek)
