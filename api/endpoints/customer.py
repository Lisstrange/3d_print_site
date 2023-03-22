from typing import List
from models import Customer
from fastapi.routing import APIRouter

router = APIRouter()


@router.get(
    "/",
    response_model=List[Customer]
)
async def get_all_customers():
    return await Customer.objects.all()

