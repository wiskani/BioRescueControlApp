from typing import List, Optional
from pydantic import BaseModel, Field


class Species (BaseModel):
    scientific_name: str = Field(..., example="Ailuropoda melanoleuca")
    common_name: str = Field( example="Giant Panda")
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


