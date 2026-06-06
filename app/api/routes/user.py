from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.schemas.user import UserResponse
from app.services.user_service import get_users
from app.core.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=list[UserResponse])
async def get_all_users(
    db: Session = Depends(get_db)
):
    return get_users(db)

@router.get("/me")
async def get_me(
    current_user = Depends(get_current_user)
):
    return {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email
        }