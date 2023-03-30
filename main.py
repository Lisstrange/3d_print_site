from fastapi import FastAPI
import uvicorn
import api
from db import BaseMeta
from utils import settings

app = FastAPI(
    title="3d_ded"
)
app.include_router(api.router)
app.state.database = BaseMeta.database


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True
    )
