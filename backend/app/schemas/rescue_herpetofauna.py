from typing import List
from pydantic import BaseModel, Field
from datetime import datetime

class AgeGroupBase(BaseModel):
    name: str = Field(..., examples=["Adulto", "Subadulto", "Juvenil"], max_length=50)
    class Config:
        orm_mode: bool = True

class AgeGroupCreate(AgeGroupBase):
    pass

class AgeGroupResponse(AgeGroupBase):
    id: int = Field(..., example=1)
    class Config:
        orm_mode: bool = True

class RescueHerpetofaunaBase(BaseModel):
    number: int = Field(..., examples=[1, 2, 3, 4, 5])
    rescue_date_in: datetime = Field(..., example="2021-01-01 00:00:00")
    rescue_date_out: datetime = Field(..., example="2021-01-01 00:00:00")
    latitude: float = Field(..., examples=[0.0, 0.0, 0.0])
    longitude: float = Field(..., examples=[0.0, 0.0, 0.0])
    altitude: int = Field(..., examples=[500,1000,2599])
    individual_count: int|None = Field(..., examples=[1, 2, 3, 4, 5])
    gender: bool|None = Field(..., examples=[True, False])
    age_group_id: int|None = Field(examples=[1, 2, 3, 4, 5])
    specie_id: int|None = Field(examples=[1, 2, 3, 4, 5])
    class Config:
        orm_mode: bool = True

class RescueHerpetofaunaCreate(RescueHerpetofaunaBase):
    pass

class RescueHerpetofaunaResponse(RescueHerpetofaunaBase):
    id: int = Field(..., example=1)
    class Config:
        orm_mode: bool = True

