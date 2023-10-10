from typing import List, Optional, Union
from pydantic import BaseModel, Field, model_validator

from app.schemas.images import ImageBase

class StatusBase (BaseModel):
    status_name: str = Field(..., examples=["Rescue"])
    class Config:
        orm_mode: bool = True

class StatusResponse (StatusBase):
    id: int = Field(...)
    class Config:
        orm_mode: bool = True


class Species (BaseModel):
    scientific_name: str = Field(..., examples=["Ailuropoda melanoleuca"])
    specific_epithet: str = Field( examples=["Panda"])
    key_gbif: int | None = Field(examples=[123456789])
    status_id: int | None = Field(examples=[1])
    genus_id: int = Field(...)
    class Config:
        orm_mode: bool = True

class SpeciesCreate (Species):
    pass

class SpeciesResponse (Species):
    id: int = Field(...)
    class Config:
        orm_mode: bool = True

class Genuses (BaseModel):
    genus_name: str = Field(..., examples=[ "Ailuropoda" ])
    key_gbif: int | None = Field(examples=[123456789])
    class Config:
        orm_mode: bool = True

class GenusesCreate (Genuses):
    family_id: int
    class Config:
        orm_mode: bool = True

class GenusesResponse (Genuses):
    id: int = Field(...)
    family_id: int = Field(...)
    class Config:
        orm_mode: bool = True

class Families (BaseModel):
    family_name: str = Field(..., examples=[ " Ursidae"])
    key_gbif: int | None = Field(examples=[123456789])
    class Config:
        orm_mode: bool = True

class FamiliesCreate (Families):
    order_id: int
    class Config:
        orm_mode: bool = True

class FamiliesResponse (Families):
    id: int = Field(...)
    order_id: int = Field(...)
    class Config:
        orm_mode: bool = True

class Orders (BaseModel):
    order_name: str = Field(..., examples=["Carnivora"])
    key_gbif: int | None = Field(examples=[123456789])
    class Config:
        orm_mode: bool = True

class OrdersResponse (Orders):
    id: int = Field(...)
    class Config:
        orm_mode: bool = True

class OrdersCreate (Orders):
    class__id: int
    class Config:
        orm_mode: bool = True

class Classes (BaseModel):
    class_name: str = Field(..., examples=["Mammalia"])
    key_gbif: Union[int, None] = Field(examples=[123456789])
    class Config:
        orm_mode: bool = True

class ClassesCreate (Classes):
    pass
    class Config:
        orm_mode: bool = True

class ClassesResponse (Classes):
    id: int = Field(...)
    class Config:
        orm_mode: bool = True

# model for global join species, genus, family, order, class and images
class SpeciesJoin (BaseModel):
    scientific_name: str = Field(..., examples=["Ailuropoda melanoleuca"])
    genus_full_name: str = Field(..., examples=["Ailuropoda melanoleuca"])
    family_name: str = Field(..., examples=["Ursidae"])
    order_name: str = Field(..., examples=["Carnivora"])
    class_name: str = Field(..., examples=["Mammalia"])
    images: List[ImageBase]
    total_rescues: int = Field(examples=[1])
    class Config:
        orm_mode: bool = True


