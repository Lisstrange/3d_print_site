from typing import List
from models import Customer
from fastapi.routing import APIRouter
import schemas
import models
from uuid import UUID

router = APIRouter()


@router.get(
    "/",
    response_model=List[Customer]
)
async def get_all_customers():
    return await Customer.objects.all()


@router.post(
    "/",
    response_model=schemas.CustomerBaseResponseSchema
)
async def create_customer(customer: schemas.CustomerCreateRequestSchema):
    return await models.Customer.objects.create(**customer.dict())


@router.get(
    "/{id}",
    response_model=schemas.CustomerBaseResponseSchema
)
async def get_customer_by_id(pk: UUID) -> Customer:
    instance = await Customer.objects.get_or_none(id=pk)
    return instance


@router.patch(
    "/{id}",
    response_model=schemas.CustomerBaseResponseSchema
)
async def update_customer_info(pk: UUID,
                               info: schemas.CustomerBaseRequestSchema):
    print(type(info))
    instance = await get_customer_by_id(pk)
    return await instance.update(**info.dict(exclude={"id"},
                                             exclude_none=True,
                                             exclude_unset=True,
                                             exclude_defaults=True,
                                             exclude_relations=True
                                             ))


@router.delete("/{id}")
async def delete_customer(pk: UUID):
    instance = await get_customer_by_id(pk)
    deleted_records = await instance.delete()
    return None
