from pydantic import (
    BaseModel,
    Field,
    field_validator
)

class UTMData(BaseModel):
    easting: float = Field(..., ge=0, le=1000000)
    northing: float = Field(..., ge=0, le=10000000)
    zone_number: int
    zone_letter: str

    @field_validator("zone_number")
    @classmethod
    def check_zone_number(cls, v) -> int:
        if v < 1 or v > 60:
            raise ValueError("Zone number must be between 1 and 60")
        return v

    @field_validator("zone_letter")
    @classmethod
    def check_zone_letter(cls, v) -> str:
        if v not in "CDEFGHJKLMNPQRSTUVWXX":
            raise ValueError("Zone letter must be between C and X")
        return v


class SpecieGbif(BaseModel):
    key: int = Field(...)
    kingdom: str = Field(...)
    phylum: str = Field(...)
    order: str = Field(...)
    family: str = Field(...)
    genus: str = Field(...)
    species: str = Field(...)
    kingdomKey: int = Field(...)
    phylumKey: int = Field(...)
    orderKey: int = Field(...)
    familyKey: int = Field(...)
    genusKey: int = Field(...)
    speciesKey: int = Field(...)
    scientificName: str = Field(...)
    canonicalName: str = Field(...)
    class_: str = Field(..., alias="class")
    classKey: int = Field(...)
