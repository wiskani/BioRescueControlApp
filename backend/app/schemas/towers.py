from pydantic import BaseModel, Field 
from datetime import datetime

class TowerBase(BaseModel):
    number: int = Field(..., example=1)
    latitude: float = Field(..., example=1.0)
    longitude: float = Field(..., example=1.0)
    class Config:
        orm_mode = True

class TowerResponse(TowerBase):
    id: int = Field(..., example=1)
    class Config:
        orm_mode = True

class ClearFloraBase(BaseModel):
    is_clear: bool = Field(..., example=True)
    tower_id: int = Field(..., example=1)
    clear_at: datetime = Field(..., example=datetime.utcnow())
    class Config:
        orm_mode = True

class ClearFloraResponse(ClearFloraBase):
    id: int = Field(..., example=1)
    class Config:
        orm_mode = True

class ClearHerpetoFaunaBase(BaseModel):
    is_clear: bool = Field(..., example=True)
    tower_id: int = Field(..., example=1)
    clear_at: datetime = Field(..., example=datetime.utcnow())
    class Config:
        orm_mode = True

class ClearHerpetoFaunaResponse(ClearHerpetoFaunaBase):
    id: int = Field(..., example=1)
    class Config:
        orm_mode = True

class ClearMammalBase(BaseModel):
    is_clear: bool = Field(..., example=True)
    tower_id: int = Field(..., example=1)
    clear_at: datetime = Field(..., example=datetime.utcnow())
    class Config:
        orm_mode = True

class ClearMammalResponse(ClearMammalBase):
    id: int = Field(..., example=1)
    class Config:
        orm_mode = True


