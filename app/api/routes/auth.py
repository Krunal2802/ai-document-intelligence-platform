from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin
from app.services.user_service import create_user, get_user_by_email
from app.db.dependencies import get_db
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/register/")
async def signup(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    new_user = create_user(
        db = db,
        name = user.name,
        email = user.email,
        password = hash_password(user.password)
    )

    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email
    }

@router.post("/login/")
async def login(
    user: UserLogin,
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

    if not verify_password(user.password, db_user.password):
        return {
            "message" : "Invalid password"
        }

    access_token = create_access_token(
        {
            "sub": db_user.email,
            "user_id": db_user.id
        }
    )

    return {
        "access_token" : access_token,
        "token_type" : "bearer"
    }