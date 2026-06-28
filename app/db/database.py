from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind = engine
)

# checking db connection
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("Database Connected Successfully!!!")
except Exception as e:
    print("Database Connection Failed", str(e))