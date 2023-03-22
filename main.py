from fastapi import FastAPI
import uvicorn
import api

app = FastAPI(
    title="3d_ded"
)
app.include_router(api.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True
    )
