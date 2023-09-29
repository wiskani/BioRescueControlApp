from typing import List, Optional
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
    status_id: int | None = Field(examples=[1])
    class Config:
        orm_mode: bool = True

class SpeciesCreate (Species):
    genus_id: int = Field(...)
    class Config:
        orm_mode: bool = True

class SpeciesResponse (Species):
    id: int = Field(...)
    genus_id: int = Field(...)
    class Config:
        orm_mode: bool = True

class Genuses (BaseModel):
    genus_name: str = Field(..., examples=[ "Ailuropoda" ])
    genus_full_name: str | None = Field(examples=[ " Ailuropoda melanoleuca"])
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


