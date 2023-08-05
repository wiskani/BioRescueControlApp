from pydantic import BaseModel, Field 
from typing import Optional, List
from datetime import datetime

class FloraRescueZoneBase(BaseModel):
    name: str = Field(..., max_length=50)
    description: str = Field(..., max_length=100)

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
    rescue_area_latitude: float = Field(example= -17.444)
    rescue_area_longitude: float= Field(example= -66.444)
    substrate: Optional [str] = Field(None, max_lengthi=50, example="Geofita")
    dap_bryophyte: Optional [float] = Field(None)
    height_bryophyte: Optional [float] = Field(None)
    bryophyte_position: Optional [int] = Field(None)
    growth_habit: str = Field( max_length=50, example="Geófito")
    epiphyte_phenology: str = Field( max_length=50, example="Esteril")
    health_status_epiphyte: str = Field( max_length=50, example="Bueno")
    microhabitat: str = Field( max_length=50, example="Bosque de ladera")
    other_observations: str = Field(max_length=100)
    specie_bryophyte_id: Optional[int]= Field(None)
    genus_bryophyte_id: Optional[int]= Field(None)
    family_bryophyte_id: Optional[int]= Field(None)
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
    cod_reg: str
    health_status_epiphyte: str = Field( max_length=50)
    vegetative_state: str = Field( max_length=50)
    flowering_date: datetime
    treatment_product: str = Field( max_length=50, example="1,2,3")
    is_pruned: bool
    is_phytosanitary_treatment:bool
    substrate: str = Field( max_length=50)
    departure_date: datetime
    flora_rescue_id: int

    class Config:
        orm_mode = True

class PlantNurseryResponse(PlantNurseryBase):
    id: int

    class Config:
        orm_mode = True

class FloraRelocationBase(BaseModel):
    relocation_date: datetime = Field(...)
    size: float
    epiphyte_phenology: str = Field( max_length=50, example="Esteril")
    johanson_zone: Optional [ str ] = Field(None, max_length=50)
    relocation_position_latitude: float
    relocation_position_longitude: float
    bryophyte_number: int = Field(...)
    dap_bryophyte: Optional [ float ]= Field(None)
    height_bryophyte:Optional [ float ] = Field(None)
    bark_type: Optional [ str ] = Field(None, max_length=50)
    infested_lianas: Optional [ str ] = Field(None, example="Poco")
    relocation_number: int = Field(...)
    other_observations: Optional [ str ] = Field(None, max_length=100)
    flora_rescue_id: int
    specie_bryophyte_id: Optional[int] = Field(default=None)
    genus_bryophyte_id: Optional[int] = Field(default=None)
    family_bryophyte_id:Optional [ int ] = Field(None)
    relocation_zone_id:  int

    class Config:
        orm_mode = True

class FloraRelocationResponse(FloraRelocationBase):
    id: int
    
    class Config:
        orm_mode = True

