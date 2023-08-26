from pydantic import BaseModel, EmailStr, Field
from typing import List

class Users(BaseModel):
    id: int
    email: EmailStr = Field(... )
    permissions: List[str] = Field(...)
    name: str = Field(...)
    last_name: str 
    class Config:
        orm_mode: bool  = True

class UsersCreate(Users):
    hashed_password: str = Field(..., min_length=7, max_length=30)
    class Config:
        orm_mode: bool  = True

class UsersResponse(BaseModel):
    id: int
    email: EmailStr = Field(...)
    class Config:
        orm_mode: bool  = True
    
