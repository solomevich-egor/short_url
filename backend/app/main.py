from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import sessionmanager
from .routers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan, docs_url="/api/docs")


@app.get("/")
async def root():
    return {"message": "Short-URL ROOT"}


app.include_router(router)
