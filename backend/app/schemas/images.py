from pydantic import BaseModel

#schema for image
class ImageBase(BaseModel):
    url: str | None
    atribute: str | None
    species_id: int
    class Config:
        from_attributes = True

#schema for image response
class ImageResponse(ImageBase):
    id: int
    class Config:
        from_attributes = True


