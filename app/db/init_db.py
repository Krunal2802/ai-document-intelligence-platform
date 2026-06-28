"""
Development utility only.

This file can be used to create all tables directly from
SQLAlchemy models for local testing or debugging.

Production schema management should be done through Alembic
migrations, not Base.metadata.create_all().

Usage:
    python -m app.db.init_db
"""

from app.db.database import engine
from app.models.base import Base

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Tables are created Successfully!!!")

init_db()