from fastapi import FastAPI
from app.api.routes.auth import router as auth_router
from app.api.routes.user import router as user_router

app = FastAPI()

app.include_router(
    auth_router,
    prefix = "/auth",
    tags = ["Authentication"]
)

app.include_router(
    user_router,
    prefix = "/user",
    tags = ["User"]
)