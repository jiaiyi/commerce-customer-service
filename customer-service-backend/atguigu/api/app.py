from fastapi import FastAPI

from atguigu.api.routers import router




app = FastAPI()

app.include_router(router)