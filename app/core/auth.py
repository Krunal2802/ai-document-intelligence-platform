from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.core.security import verify_access_token
from app.services.user_service import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl = "/auth/login" ## Tells Swagger -> This endpoint issues tokens. You see authorize button on swagger in top right corner
)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code = 401,
            detail = "Invalid Token"
        )

    email = payload.get("sub")
    user = get_user_by_email(db = db, email = email)

    if user is None:
        raise HTTPException(
            status_code = 401,
            detail = "User Not Found"
        )

    return user