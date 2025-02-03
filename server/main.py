from fastapi import FastAPI
from db.db import init_db
from .routes.users.router import router as router_users
from .routes.imei_api.router import router as router_imei

app = FastAPI()


@app.middleware("http")
async def startup_event(request, call_next):
    if request.method == "GET" and request.url.path == "/":
        await init_db()
    response = await call_next(request)
    return response

app.include_router(router_users)
app.include_router(router_imei)