from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    
    model_config = ConfigDict(
        from_attributes=True # Meaning: when fastAPI retun SQLAlchemy Object, Pydantic needs to know it should read attributes from the ORM object.
    )