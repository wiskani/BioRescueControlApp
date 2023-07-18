from typing import List, Optional
from pydantic import BaseModel, Field

#schema for image
class ImageBase(BaseModel):
    url: str
    class Config:
        orm_mode = True

#schema for image response
class ImageResponse(ImageBase):
    id: int
    class Config:
        orm_mode = True


