from typing import (
        List,
        )
from pydantic import (
    BaseModel,
    Field,
        )

class SunburstBase(BaseModel):
    name: str = Field(..., examples=["nivo"])
    color: str = Field(..., examples=["hsl(335, 70%, 50%)"])
    loc: int|None
    children: List["SunburstBase"]|None 

SunburstBase.model_rebuild()

