from typing import List
from pydantic import (
    BaseModel,
    Field,
    model_validator,
    )
from fastapi import HTTPException
from datetime import datetime

class HabitatBase(BaseModel):
    name: str = Field(..., examples=["Bosque de Polylepis"], max_length=50)
    class Config:
        orm_mode: bool = True

class HabitatCreate(HabitatBase):
    pass

class HabitatResponse(HabitatBase):
    id: int
    class Config:
        orm_mode: bool = True

class RescueMammalsBase(BaseModel):
    cod: str = Field(..., examples=[ "1" ])
    date: datetime = Field(..., examples=[ datetime.now() ])
    mark: str = Field(..., examples=[ "1" ])
    longitude: float = Field(..., examples=[ 1.0 ])
    latitude: float = Field(..., examples=[ 1.0 ])
    altitude: int = Field(..., examples=[ 1 ])
    gender: bool|None = Field(examples=[True])
    LT: float|None = Field(examples=[1.0])
    LC: float|None = Field(examples=[1.0])
    LP: float|None = Field(examples=[1.0])
    LO: float|None = Field(examples=[1.0])
    LA: float|None = Field(examples=[1.0])
    weight: float|None = Field(examples=[1.0])
    observation: str|None = Field(examples=["Observacion"])
    is_specie_confirmed: bool = Field(..., examples=[True])
    habitat_id: int = Field(..., examples=[ 1 ])
    age_group_id: int|None = Field(examples=[ 1 ])
    specie_id: int|None = Field(examples=[ 1 ])
    genus_id: int|None = Field(examples=[ 1 ])
    class Config:
        orm_mode: bool = True

    @model_validator(mode='after')
    def check_taxon_bryophyte(self):
        if self.specie_id:
            if self.genus_id:
                raise HTTPException(
                    status_code=400,
                    detail="if specie exists, genus must be null"
                )
        elif self.genus_id is None and self.specie_id is None:
             raise HTTPException(
                 status_code=400,
                 detail="specie or genus must be not null"
                )
        return self

class RescueMammalsCreate(RescueMammalsBase):
    pass

class RescueMammalsResponse(RescueMammalsBase):
    id: int
    class Config:
        orm_mode: bool = True

class SiteReleaseMammalsBase(BaseModel):
    name: str = Field(..., examples=["Sitio de liberacion"], max_length=50)
    class Config:
        orm_mode: bool = True

class SiteReleaseMammalsCreate(SiteReleaseMammalsBase):
    pass

class SiteReleaseMammalsResponse(SiteReleaseMammalsBase):
    id: int
    class Config:
        orm_mode: bool = True

class ReleaseMammalsBase(BaseModel):
    cod: str = Field(..., examples=[ "1" ])
    longitude: float|None = Field( examples=[ 1.0 ])
    latitude: float|None = Field( examples=[ 1.0 ])
    altitude: int|None = Field( examples=[ 1 ])
    sustrate: str|None = Field(examples=["Sustrato"])
    site_release_mammals_id: int = Field(..., examples=[ 1 ])
    rescue_mammals_id: int = Field(..., examples=[ 1 ])
    class Config:
        orm_mode: bool = True

class ReleaseMammalsCreate(ReleaseMammalsBase):
    pass

class ReleaseMammalsResponse(ReleaseMammalsBase):
    id: int
    class Config:
        orm_mode: bool = True


class RescueMammalsWithSpecie(BaseModel):
    cod: str 
    date: datetime 
    longitude: float 
    latitude: float 
    observation: str|None 
    specie_name: str | None
    genus_name: str | None
    class Config:
        orm_mode: bool = True
