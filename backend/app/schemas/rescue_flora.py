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

    class Config:
        orm_mode = True

class FloraRelocationZoneBase(BaseModel):
    name: str = Field(..., max_length=50)

    class Config:
        orm_mode = True

class FloraRelocationZoneResponse(FloraRelocationZoneBase):
    id: int

    class Config:
        orm_mode = True

class FloraRescueBase(BaseModel):
    epiphyte_number: int = Field(...)
    rescue_date: datetime = Field(...)
    rescue_area_latitude: float
    rescue_area_longitude: float
    dap_bryophyte: float
    height_bryophyte: float
    bryophyte_position: int 
    growth_habit: str = Field( max_length=50)
    epiphyte_phenology: str = Field( max_length=50)
    health_status_epiphyte: str = Field( max_length=50)
    other_observations: str = Field(max_length=100)
    specie_bryophyte_id: int
    specie_epiphyte_id: int
    rescue_zone_id: int

    class Config:
        orm_mode = True

class FloraRescueResponse(FloraRescueBase):
    id: int

    class Config:
        orm_mode = True

class PlantNurseryBase(BaseModel):
    entry_date: datetime = Field(...)
    cod_reg: int
    health_status_epiphyte: str = Field( max_length=50)
    flowering_date: datetime 
    treatment_product: str = Field( max_length=50)
    is_phytosanitary_treatment: bool
    substrate: str = Field( max_length=50)
    departure_date: datetime
    flora_rescue_id: int = Field(...)
    specie_id: int
    relaction_zone_id: int

    class Config:
        orm_mode = True

class PlantNurseryResponse(PlantNurseryBase):
    id: int

    class Config:
        orm_mode = True

class FloraRelocationBase(BaseModel):
    relocation_date: datetime = Field(...)
    size: float
    epiphyte_phenology: str = Field( max_length=50)
    johanson_zone: str = Field( max_length=50)
    relocation_position_latitude: float
    relocation_position_longitude: float
    bryophyte_number: int = Field(...)
    dap_bryophyte: float
    height_bryophyte: float
    bryophyte_position: int
    bark_type: str = Field( max_length=50)
    is_infested_lianas: bool
    relocation_number: int = Field(...)
    other_observations: str = Field(max_length=100)
    resccue_zone_id: int
    flora_rescue_id: int
    specie_bryophyte_id: int
    relaction_zone_id: int

    class Config:
        orm_mode = True

class FloraRelocationResponse(FloraRelocationBase):
    id: int
    
    class Config:
        orm_mode = True

