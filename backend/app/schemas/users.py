#Pydantic
from pydantic import BaseModel, EmailStr, Field

class Users(BaseModel):
    id: int
    email: EmailStr = Field(..., max_length=254)
    class Config:
        orm_mode: bool  = True

class UsersCreate(Users):
    password: str = Field(..., min_length=7, max_length=30)

class UsersResponse(BaseModel):
    id: int
    email: EmailStr = Field(..., max_length=254)
    class Config:
        orm_mode: bool  = True
    
