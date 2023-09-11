from pydantic import BaseModel, Field 
from datetime import datetime

class TowerBase(BaseModel):
    number: int = Field(..., examples=[1])
    latitude: float = Field(..., examples=[1.0])
    longitude: float = Field(..., examples=[1.0])
    class Config:
        orm_mode = True

class TowerResponse(TowerBase):
    id: int = Field(..., examples=[1])
    class Config:
        orm_mode = True

class ClearFloraBase(BaseModel):
    is_clear: bool = Field(..., examples=[False])
    clear_at: datetime = Field(..., examples=[datetime.utcnow()])
    class Config:
        orm_mode = True

class ClearFloraResponse(ClearFloraBase):
    id: int = Field(..., examples=[1])
    tower_id: int = Field(..., examples=[1])
    class Config:
        orm_mode = True

class ClearHerpetoFaunaBase(BaseModel):
    is_clear: bool = Field(..., examples=[False])
    clear_at: datetime = Field(..., examples=[datetime.utcnow()])
    class Config:
        orm_mode = True

class ClearHerpetoFaunaResponse(ClearHerpetoFaunaBase):
    id: int = Field(..., examples=[1])
    tower_id: int = Field(..., examples=[1])
    class Config:
        orm_mode = True

class ClearMammalBase(BaseModel):
    is_clear: bool = Field(..., examples=[False])
    clear_at: datetime = Field(..., examples=[datetime.utcnow()])
    class Config:
        orm_mode = True

class ClearMammalResponse(ClearMammalBase):
    id: int = Field(..., examples=[1])
    tower_id: int = Field(..., examples=[1])
    class Config:
        orm_mode = True


