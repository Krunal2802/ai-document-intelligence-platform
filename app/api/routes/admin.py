from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.schemas.user import UserResponse
from app.services.user_service import get_users

router = APIRouter()

@router.get("/users/", response_model=list[UserResponse])
async def get_all_users(
    db: Session = Depends(get_db)
):
    return get_users(db)