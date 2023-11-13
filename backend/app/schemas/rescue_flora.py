from pydantic import BaseModel, Field
from datetime import datetime

class FloraRescueZoneBase(BaseModel):
    name: str = Field(..., max_length=50)
    description: str = Field(..., max_length=100)

    class Config:
        from_attributes = True


class FloraRescueZoneResponse(FloraRescueZoneBase):
    id: int

    class Config:
        from_attributes = True

class FloraRelocationZoneBase(BaseModel):
    name: str = Field(..., max_length=50)

    class Config:
        from_attributes = True

class FloraRelocationZoneResponse(FloraRelocationZoneBase):
    id: int

    class Config:
        from_attributes = True

class FloraRescueBase(BaseModel):
    epiphyte_number: str = Field(...)
    rescue_date: datetime = Field(...)
    rescue_area_latitude: float = Field(examples= [-17.444])
    rescue_area_longitude: float= Field(examples= [-66.444])
    substrate: str | None = Field(max_lengthi=50, examples=["Geofita"])
    dap_bryophyte: float | None
    height_bryophyte: float | None
    bryophyte_position: int | None
    growth_habit: str = Field( max_length=50, examples=["Geófito"])
    epiphyte_phenology: str = Field( max_length=50, examples=["Esteril"])
    health_status_epiphyte: str = Field( max_length=50, examples=["Bueno"])
    microhabitat: str = Field( max_length=50, examples=["Bosque de ladera"])
    other_observations: str = Field(max_length=100)
    specie_bryophyte_id: int | None
    genus_bryophyte_id: int | None
    family_bryophyte_id: int | None
    specie_epiphyte_id: int
    rescue_zone_id: int

    class Config:
        from_attributes = True

class FloraRescueResponse(FloraRescueBase):
    id: int

    class Config:
        from_attributes = True

class PlantNurseryBase(BaseModel):
    entry_date: datetime = Field(...)
    cod_reg: str
    health_status_epiphyte: str = Field( max_length=50)
    vegetative_state: str = Field( max_length=50)
    flowering_date: datetime
    treatment_product: str = Field( max_length=50, examples=["1,2,3"])
    is_pruned: bool
    is_phytosanitary_treatment:bool
    substrate: str = Field( max_length=50)
    departure_date: datetime
    flora_rescue_id: int

    class Config:
        from_attributes = True

class PlantNurseryResponse(PlantNurseryBase):
    id: int

    class Config:
        from_attributes = True

class FloraRelocationBase(BaseModel):
    relocation_date: datetime = Field(...)
    size: float
    epiphyte_phenology: str = Field( max_length=50, examples=["Esteril"])
    johanson_zone: str | None = Field(max_length=50)
    relocation_position_latitude: float
    relocation_position_longitude: float
    bryophyte_number: int = Field(...)
    dap_bryophyte: float | None
    height_bryophyte: float | None
    bark_type:  str | None  = Field(max_length=50)
    infested_lianas: str | None = Field(examples=["Poco"])
    relocation_number: int = Field(...)
    other_observations:  str | None = Field(max_length=100)
    flora_rescue_id: int
    specie_bryophyte_id: int | None  = Field(default=None)
    genus_bryophyte_id: int | None = Field(default=None)
    family_bryophyte_id:  int | None
    relocation_zone_id:  int

    class Config:
        from_attributes = True

class FloraRelocationResponse(FloraRelocationBase):
    id: int

    class Config:
        from_attributes = True

