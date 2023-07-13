from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class FloraRescueZoneBase(BaseModel):
    name: str = Field(..., max_length=50)
    description: str = Field(..., max_length=100)
    latitude: float
    longitude: float

    class Config:
        orm_mode = True


class FloraRescueZoneResponse(FloraRescueZoneBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class FloraRescue(BaseModel):
    epiphyte_number: int = Field(...)
    rescue_date: datetime = Field(...)
    rescue_area_latitude: float
    rescue_area_longitude: float
    dap_bryophyte: float
    height_bryophyte: float
    bryophyte_position: float
    growth_habit: str = Field( max_length=50)
    epiphyte_phenology: str = Field( max_length=50)
    health_status_epiphyte: str = Field( max_length=50)
    other_observations: str = Field(max_length=100)
    specie_bryophyte_id: int
    specie_epiphyte_id: int
    rescue_zone_id: int

    class Config:
        orm_mode = True

class FloraRescueResponse(FloraRescue):
    id: int

    class Config:
        orm_mode = True
