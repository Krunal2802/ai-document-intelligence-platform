from sqlalchemy.orm import Session
from app.models.user import User

class UserService:

    def __init__(self, db: Session):
        self.db = db

    def create_user(
        self,
        name: str, 
        email: str,
        password: str
    ):

        user = User(name = name, email = email, password = password)

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def get_user_by_email(
        self,
        email: str
    ):
        return (
            self.db.query(User).filter(User.email == email).first()
        )

    def get_users(self):
        return self.db.query(User).all()