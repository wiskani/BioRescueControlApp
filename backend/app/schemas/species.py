from typing import List, Optional
from pydantic import BaseModel, Field

from app.schemas.images import ImageBase


class Species (BaseModel):
    scientific_name: str = Field(..., example="Ailuropoda melanoleuca")
    specific_epithet: str = Field( example="Panda")
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
    genus_name: str = Field(..., example="Ailuropoda")
    genus_full_name: str = Field(None, example="Ailuropoda melanoleuca")
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
    family_name: str = Field(..., example="Ursidae")
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
    order_name: str = Field(..., example="Carnivora")
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
    class_name: str = Field(..., example="Mammalia")
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
    scientific_name: str = Field(..., example="Ailuropoda melanoleuca")
    genus_full_name: str = Field(..., example="Ailuropoda melanoleuca")
    family_name: str = Field(..., example="Ursidae")
    order_name: str = Field(..., example="Carnivora")
    class_name: str = Field(..., example="Mammalia")
    images: List[ImageBase] 
    total_rescues: int = Field(example=1)
    class Config:
        orm_mode: bool = True


