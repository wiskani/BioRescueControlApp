from pydantic import BaseModel, EmailStr, Field

class Species (BaseModel):
    scientific_name: str = Field(..., example="Ailuropoda melanoleuca")
    common_name: str = Field( example="Giant Panda")
    class Config:
        orm_mode: bool = True
