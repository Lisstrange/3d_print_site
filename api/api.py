from fastapi.routing import APIRouter
from .endpoints import user, order, auth

router = APIRouter(prefix="/api/v1")

router.include_router(user.router, prefix="/user", tags=["User"])
router.include_router(order.router, prefix="/order", tags=["Order"])
router.include_router(auth.router, prefix="/auth", tags=["Auth"])
