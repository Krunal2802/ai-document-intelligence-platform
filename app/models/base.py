from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Base acts as the parent class for all SQLAlchemy models. 
# It stores metadata about tables and allows SQLAlchemy to create database schemas.