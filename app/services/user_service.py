from sqlalchemy.orm import Session
from app.models.user_model import User

def create_user(
    db: Session,
    name: str, 
    email: str,
    password: str
):

    user = User(name = name, email = email, password = password)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user