from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user_schema import CreateUser, userLogin
from app.services.user_service import create_user, get_user_by_email
from app.db.dependencies import get_db

router = APIRouter()

@router.get("/")
async def check():
    return {"message":"user router is working!!!"}

@router.post("/signup/")
async def signup(
    user: CreateUser,
    db: Session = Depends(get_db)
):
    new_user = create_user(
        db = db,
        name = user.name,
        email = user.email,
        password = user.password
    )

    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email
    }

@router.post("/login/")
async def login(
    user: userLogin,
    db: Session = Depends(get_db)
    ):
    db_user = get_user_by_email(
        db = db,
        email = user.email
    )

    if not db_user:
        return {
            "message":"User Not Found"
        }

    if db_user.password != user.password:
        return {
            "message" : "Invalid password"
        }

    return {
        "message":"Login Successful!!!"
    }