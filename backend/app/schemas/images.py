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

#schema for image create withou url
class ImageCreate(BaseModel):
    atribute: str | None = Field(...)
    species_id: int = Field(...)

    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value)) 
        return value







