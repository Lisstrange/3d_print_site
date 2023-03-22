from fastapi.routing import APIRouter
from models import Order
from typing import List

router = APIRouter()


@router.get("/",
            response_model=List[Order])
async def get_all_orders():
    return await Order.objects.all()
