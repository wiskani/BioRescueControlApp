from pydantic import BaseModel, Field, model_validator
import json

#schema for image
class ImageBase(BaseModel):
    url: str | None
    atribute: str | None
    species_id: int
    class Config:
        orm_mode: bool = True

#schema for image response
class ImageResponse(ImageBase):
    id: int
    class Config:
        orm_mode: bool = True








