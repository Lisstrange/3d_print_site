from fastapi.routing import APIRouter
from .endpoints import customer, order

router = APIRouter(prefix="/api/v1")

router.include_router(customer.router, prefix="/customer")
router.include_router(order.router, prefix="/order")
