from app.db.database import engine
from app.models.base import Base
from app.models.user_model import User

Base.metadata.create_all(bind=engine)

print("Tables are created Successfully!!!")