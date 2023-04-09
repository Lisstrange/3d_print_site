from uuid import UUID, uuid4
from fastapi import File, UploadFile, FastAPI
from fastapi.routing import APIRouter
from models import Order
from typing import List
import schemas
from .user import get_user_by_id

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
             response_model=schemas.OrderBaseResponseSchema)
async def create_order(order: schemas.OrderCreateRequestSchema,
                       user_id: UUID
                       # TODO добавить звагрузку файа     content = await upload_file.read()
                       # И сгенерить норм схему на его основе
                       ):

    instance = await get_user_by_id(user_id)
    return await Order.objects.create(user=instance, **order.dict())


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
