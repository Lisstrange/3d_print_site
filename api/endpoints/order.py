from uuid import UUID, uuid4

from fastapi.routing import APIRouter
from models import Order
from typing import List
import schemas
from .customer import get_customer_by_id

router = APIRouter()


@router.get("/",
            response_model=List[Order])
async def get_all_orders():
    return await Order.objects.all()


@router.get("/{id}",
            response_model=schemas.OrderBaseResponseSchema)
async def get_order_by_id(pk: UUID):
    return await Order.filter(id=pk)


@router.post("/",
             response_model=Order)
async def create_order(order: schemas.OrderCreateRequestSchema, customer_id: UUID):
    customer = await get_customer_by_id(customer_id)
    return await Order.objects.create(customer=customer, **order.dict())


@router.patch("/{id}",
              response_model=Order)
async def update_order_info(pk: UUID,
                            info: Order) -> Order:
    instance = await get_order_by_id(pk)
    return await instance.update(**info.dict(exclude={"id"},
                                             exclude_unset=True,
                                             exclude_none=True,
                                             exclude_defaults=True))


@router.delete("/{id}")
async def delete_order(pk: UUID):
    instance = await get_order_by_id(pk)
    return await instance.delete()
# TODO дописать методы вызова запросов!
