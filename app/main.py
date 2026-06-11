from fastapi import FastAPI
from app.api.routes.auth import router as auth_router
from app.api.routes.admin import router as admin_router

app = FastAPI()

app.include_router(
    auth_router,
    prefix = "/auth",
    tags = ["Authentication"]
)

app.include_router(
    admin_router,
    prefix = "/admin",
    tags = ["User"]
)