from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.user_service import UserService
from app.db.dependencies import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.core.auth import get_current_user

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def signup(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    user_service = UserService(db)

    check_email_exists = user_service.get_user_by_email(user.email)

    if check_email_exists:
        return {
            "message": "This email is used already, use different email."
        }
        
    new_user = user_service.create_user(
        name = user.name,
        email = user.email,
        password = hash_password(user.password)
    )

    return new_user

@router.post("/login")
async def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    user_service = UserService(db)

    db_user = user_service.get_user_by_email(
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

@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user = Depends(get_current_user)
):
    return current_user