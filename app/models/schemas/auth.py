# app/models/schemas/auth.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True  # lets this be built directly from a SQLAlchemy User object

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"