from pydantic import (
    BaseModel,
    Field,
    model_validator,
    )

from fastapi import HTTPException
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
    rescue_area_latitude: float = Field(examples=[-17.444])
    rescue_area_longitude: float = Field(examples=[-66.444])
    substrate: str | None = Field(max_length=50, examples=["Geofita"])
    dap_bryophyte: float | None
    height_bryophyte: float | None
    bryophyte_position: int | None
    growth_habit: str | None = Field(max_length=50, examples=["Geófito"])
    epiphyte_phenology: str | None = Field(max_length=50, examples=["Esteril"])
    health_status_epiphyte: str | None = Field(
            max_length=50,
            examples=["Bueno"]
            )
    microhabitat: str | None = Field(
            max_length=100,
            examples=["Bosque de ladera"]
            )
    other_observations: str | None = Field(max_length=100)
    is_epiphyte_confirmed: bool = Field(...)
    is_bryophyte_confirmed: bool = Field(...)
    specie_bryophyte_id: int | None
    genus_bryophyte_id: int | None
    family_bryophyte_id: int | None
    specie_epiphyte_id: int | None
    genus_epiphyte_id: int | None
    family_epiphyte_id: int | None
    rescue_zone_id: int

    class Config:
        from_attributes = True

    @model_validator(mode='after')
    def check_taxon_bryophyte(self):
        if self.specie_bryophyte_id:
            if self.genus_bryophyte_id or self.family_bryophyte_id:
                raise HTTPException(
                    status_code=400,
                    detail="if specie bryophite exists, genus and family must be null"
                )
        elif self.genus_bryophyte_id:
            if self.specie_bryophyte_id or self.family_bryophyte_id:
                raise HTTPException(
                    status_code=400,
                    detail="if genus bryophite exists, specie and family must be null"
                )
        elif self.family_bryophyte_id:
            if self.specie_bryophyte_id or self.genus_bryophyte_id:
                raise HTTPException(
                    status_code=400,
                    detail="if family bryophite exists, specie and genus must be null"
                )
        return self

    @model_validator(mode='after')
    def check_taxon_epiphyte(self):
        if self.specie_epiphyte_id:
            if self.genus_epiphyte_id or self.family_epiphyte_id:
                raise HTTPException(
                    status_code=400,
                    detail="if specie epiphyte exists, genus and family must be null"
                )
        elif self.genus_epiphyte_id:
            if self.specie_epiphyte_id or self.family_epiphyte_id:
                raise HTTPException(
                    status_code=400,
                    detail="if genus epiphyte exists, specie and family must be null"
                )
        elif self.family_epiphyte_id:
            if self.specie_epiphyte_id or self.genus_epiphyte_id:
                raise HTTPException(
                    status_code=400,
                    detail="if family epiphyte exists, specie and genus must be null"
                )
        else:
            raise HTTPException(
                status_code=400,
                detail="specie, genus or family epiphyte must be not null"
            )
        return self


class FloraRescueResponse(FloraRescueBase):
    id: int

    class Config:
        from_attributes = True


class PlantNurseryBase(BaseModel):
    entry_date: datetime = Field(...)
    cod_reg: str
    health_status_epiphyte: str | None = Field(max_length=50)
    vegetative_state: str | None = Field(max_length=50)
    flowering_date: datetime | None
    treatment_product: str | None = Field(max_length=50, examples=["1,2,3"])
    is_pruned: bool
    is_phytosanitary_treatment: bool
    substrate: str | None = Field(max_length=50)
    departure_date: datetime | None
    flora_rescue_id: int

    class Config:
        from_attributes = True


class PlantNurseryResponse(PlantNurseryBase):
    id: int

    class Config:
        from_attributes = True


class FloraRelocationBase(BaseModel):
    relocation_date: datetime = Field(...)
    relocation_number: str = Field(...)
    size: float
    epiphyte_phenology: str = Field(max_length=50, examples=["Esteril"])
    johanson_zone: str | None = Field(max_length=50)
    relocation_position_latitude: float
    relocation_position_longitude: float
    relocation_position_altitude: int
    bryophyte_number: int = Field(...)
    dap_bryophyte: float | None
    height_bryophyte: float | None
    bark_type:  str | None = Field(max_length=50)
    infested_lianas: str | None = Field(examples=["Poco"])
    other_observations:  str | None = Field(max_length=100)
    is_bryophyte_confirmed: bool = Field(...)
    flora_rescue_id: int
    specie_bryophyte_id: int | None = Field(default=None)
    genus_bryophyte_id: int | None = Field(default=None)
    family_bryophyte_id:  int | None = Field(default=None)
    relocation_zone_id:  int

    class Config:
        from_attributes = True

    @model_validator(mode='after')
    def check_taxon_bryophyte(self):
        if self.specie_bryophyte_id:
            if self.genus_bryophyte_id or self.family_bryophyte_id:
                raise HTTPException(
                    status_code=400,
                    detail="if specie bryophite exists, genus and family must be null"
                )
        elif self.genus_bryophyte_id:
            if self.specie_bryophyte_id or self.family_bryophyte_id:
                raise HTTPException(
                    status_code=400,
                    detail="if genus bryophite exists, specie and family must be null"
                )
        elif self.family_bryophyte_id:
            if self.specie_bryophyte_id or self.genus_bryophyte_id:
                raise HTTPException(
                    status_code=400,
                    detail="if family bryophite exists, specie and genus must be null"
                )
        return self


class FloraRelocationResponse(FloraRelocationBase):
    id: int

    class Config:
        from_attributes = True


class FloraRescueSpecies(BaseModel):
    epiphyte_number: str
    rescue_date: datetime
    rescue_area_latitude: float
    rescue_area_longitude: float
    specie_name: str | None
    genus_name: str | None
    family_name: str | None
    substrate: str | None
    dap_bryophyte: float | None
    height_bryophyte: float | None
    bryophyte_position: int | None
    growth_habit: str | None
    epiphyte_phenology: str | None
    health_status_epiphyte: str | None
    microhabitat: str | None
    other_observations: str | None
    is_epiphyte_confirmed: bool
    is_bryophyte_confirmed: bool
    specie_bryophyte_name: str | None
    genus_bryophyte_name: str | None
    family_bryophyte_name: str | None


class FloraRelocationWithSpecie (BaseModel):
    relocation_date: datetime
    flora_rescue: str
    specie_name_epiphyte: str | None
    genus_name_epiphyte: str | None
    family_name_epiphyte: str | None
    size: float
    epiphyte_phenology: str
    johanson_zone: str | None
    relocation_position_latitude: float
    relocation_position_longitude: float
    relocation_position_altitude: int
    dap_bryophyte: float | None
    height_bryophyte: float | None
    bark_type:  str | None
    infested_lianas: str | None
    other_observations:  str | None
    specie_name_bryophyte: str | None
    genus_name_bryophyte: str | None
    family_name_bryophyte: str | None
    relocation_zone: str
