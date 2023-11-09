from typing import List
from pydantic import BaseModel, Field
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
    habitat_id: int = Field(..., examples=[ 1 ])
    age_group_id: int|None = Field(examples=[ 1 ])
    species_id: int = Field(..., examples=[ 1 ])
    class Config:
        orm_mode: bool = True

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
    longitude: float = Field(..., examples=[ 1.0 ])
    latitude: float = Field(..., examples=[ 1.0 ])
    altitude: int = Field(..., examples=[ 1 ])
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

