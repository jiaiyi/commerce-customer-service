from contextlib import asynccontextmanager

from fastapi import FastAPI

from atguigu.api.routers import router
from atguigu.infrastructure.database import init_db_engine_and_session_factory, close_db_engine
from atguigu.infrastructure.http_util import init_http_client, close_http_client


@asynccontextmanager
async def fn(app: FastAPI):
    init_db_engine_and_session_factory()
    init_http_client()
    yield
    await close_http_client()
    await close_db_engine()

app = FastAPI(lifespan=fn)

app.include_router(router)