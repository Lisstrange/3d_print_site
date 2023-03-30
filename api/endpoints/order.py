from uuid import UUID, uuid4

from fastapi.routing import APIRouter
from models import Order
from typing import List

router = APIRouter()


@router.get("/",
            response_model=List[Order])
async def get_all_orders():
    return await Order.objects.all()


@router.get("/{id}",
            response_model=Order)
async def get_order_by_id(pk: UUID):
    return await Order.objects.get_or_none(pk)
#
# @router.post("/",
#              response_model=Order)
# async def create_order(order: Order):
#
#TODO дописать методы вызова запросов!