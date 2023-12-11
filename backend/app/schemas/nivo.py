from typing import (
        List,
        )
from pydantic import (
    BaseModel,
    Field,
    field_validator
        )

class SunburstBase(BaseModel):
    name: str = Field(..., examples=["nivo"])
    color: str = Field(..., examples=["hsl(335, 70%, 50%)"])
    loc: int|None
    children: List["SunburstBase"]|None 

SunburstBase.model_rebuild()

class ColorHSLBase(BaseModel):
    h: int = Field(..., examples=[335])
    s: int = Field(..., examples=[70])
    l: int = Field(..., examples=[50])

    @field_validator("h")
    @classmethod
    def h_validator(cls, v):
        if v < 0 or v > 360:
            raise ValueError("h must be between 0 and 360")
        return v


    @field_validator("s")
    @classmethod
    def s_validator(cls, v):
        if v < 0 or v > 100:
            raise ValueError("s must be between 0 and 100")
        return v

    @field_validator("l")
    @classmethod
    def l_validator(cls, v):
        if v < 0 or v > 100:
            raise ValueError("l must be between 0 and 100")
        return v


