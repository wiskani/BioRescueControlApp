from typing import List
from pydantic import BaseModel, Field
from datetime import datetime


class AgeGroupBase(BaseModel):
    name: str = Field(
            ...,
            examples=["Adulto", "Subadulto", "Juvenil"],
            max_length=50
            )

    class Config:
        orm_mode: bool = True


class AgeGroupCreate(AgeGroupBase):
    pass


class AgeGroupResponse(AgeGroupBase):
    id: int

    class Config:
        orm_mode: bool = True


class TransectHerpetofaunaBase(BaseModel):
    number: str = Field(..., examples=[1])
    date_in: datetime = Field(..., examples=[datetime.now()])
    date_out: datetime = Field(..., examples=[datetime.now()])
    latitude_in: float = Field(..., examples=[1.0])
    longitude_in: float = Field(..., examples=[1.0])
    altitude_in: int = Field(..., examples=[1])
    latitude_out: float = Field(..., examples=[1.0])
    longitude_out: float = Field(..., examples=[1.0])
    altitude_out: int = Field(..., examples=[1])
    tower_id: int = Field(..., examples=[1])

    class Config:
        orm_mode: bool = True


class TransectHerpetofaunaCreate(TransectHerpetofaunaBase):
    pass


class TransectHerpetofaunaResponse(TransectHerpetofaunaBase):
    id: int

    class Config:
        orm_mode: bool = True


class MarkHerpetofaunaBase(BaseModel):
    date: datetime = Field(..., examples=[datetime.now()])
    number: int = Field(..., examples=[1])
    code: str | None = Field(examples=["1a"])
    LHC: float | None = Field(examples=[1.0])
    weight: float | None = Field(examples=[1.0])
    is_photo_mark: bool = Field(default=False)
    is_elastomer_mark: bool = Field(default=False)
    rescue_herpetofauna_id: int = Field(examples=[1])


class MarkHerpetofaunaCreate(MarkHerpetofaunaBase):
    pass


class MarkHerpetofaunaResponse(MarkHerpetofaunaBase):
    id: int

    class Config:
        orm_mode: bool = True


class RescueHerpetofaunaBase(BaseModel):
    number: str = Field(..., examples=[1])
    gender: bool | None = Field(examples=[True])
    specie_id: int = Field(..., examples=[1])
    transect_herpetofauna_id: int = Field(..., examples=[1])
    age_group_id: int | None = Field(examples=[1])

    class Config:
        orm_mode: bool = True


class RescueHerpetofaunaCreate(RescueHerpetofaunaBase):
    pass


class RescueHerpetofaunaResponse(RescueHerpetofaunaBase):
    id: int

    class Config:
        orm_mode: bool = True


class TransectHerpetofaunaTranslocationBase(BaseModel):
    cod: str = Field(..., examples=["1"])
    date: datetime = Field(..., examples=[datetime.now()])
    latitude_in: float = Field(..., examples=[1.0])
    longitude_in: float = Field(..., examples=[1.0])
    altitude_in: int = Field(..., examples=[1])
    latitude_out: float = Field(..., examples=[1.0])
    longitude_out: float = Field(..., examples=[1.0])
    altitude_out: int = Field(..., examples=[1])

    class Config:
        orm_mode: bool = True


class TransectHerpetofaunaTranslocationCreate(
        TransectHerpetofaunaTranslocationBase
        ):
    pass


class TransectHerpetofaunaTranslocationResponse(
        TransectHerpetofaunaTranslocationBase
        ):
    id: int

    class Config:
        orm_mode: bool = True


class PointHerpetofaunaTranslocationBase(BaseModel):
    cod: str = Field(..., examples=["1"])
    date: datetime = Field(..., examples=[datetime.now()])
    latitude: float = Field(..., examples=[1.0])
    longitude: float = Field(..., examples=[1.0])
    altitude: int = Field(..., examples=[1])

    class Config:
        orm_mode: bool = True


class PointHerpetofaunaTranslocationCreate(
        PointHerpetofaunaTranslocationBase
        ):
    pass


class PointHerpetofaunaTranslocationResponse(
        PointHerpetofaunaTranslocationBase
        ):
    id: int

    class Config:
        orm_mode: bool = True


class TranslocationHerpetofaunaBase(BaseModel):
    cod: str = Field(..., examples=["1"])
    transect_herpetofauna_translocation_id: int | None = Field(examples=[1])
    point_herpetofauna_translocation_id: int | None = Field(examples=[1])
    specie_id: int = Field(..., examples=[1])
    mark_herpetofauna_id: int | None = Field(examples=[1])

    class Config:
        orm_mode: bool = True


class TranslocationHerpetofaunaCreate(TranslocationHerpetofaunaBase):
    pass


class TranslocationHerpetofaunaResponse(TranslocationHerpetofaunaBase):
    id: int

    class Config:
        orm_mode: bool = True


class TransectHerpetoWithSpecies(BaseModel):
    number: str
    date_in: datetime
    date_out: datetime
    latitude_in: float
    longitude_in: float
    latitude_out: float
    longitude_out: float
    specie_names: List[str]
    total_rescue: int


class TransectHerpetoTransWithSpecies(BaseModel):
    cod: str
    date: datetime
    latitude_in: float
    longitude_in: float
    altitude_in: int
    latitude_out: float
    longitude_out: float
    altitude_out: int
    specie_names: List[str]
    total_translocation: int


class PointHerpetoTransloWithSpecies(BaseModel):
    cod: str
    date: datetime
    latitude: float
    longitude: float
    altitude: int
    specie_names: List[str]
    total_translocation: int


class RescueHerpetoWithSpecies(BaseModel):
    number: str = Field(...,)
    date_rescue: datetime
    gender: str | None
    specie_name: str
    age_group_name: str | None
    altitude_in: int
    latitude_in: float
    longitude_in: float
    altitude_out: int
    latitude_out: float
    longitude_out: float


class TransectTranslocationHerpetoWithMark(BaseModel):
    cod: str = Field(...,)
    date: datetime
    latitude_in: float
    longitude_in: float
    latitude_out: float
    longitude_out: float
    number_mark: int
    code_mark: str | None
    LHC: float | None
    weight: float | None
    is_photo_mark: bool
    is_elastomer_mark: bool


class PointTranslocationHerpetoWithMark(BaseModel):
    cod: str = Field(...,)
    date: datetime
    latitude: float
    longitude: float
    altitude: int
    number_mark: int
    code_mark: str | None
    LHC: float | None
    weight: float | None
    is_photo_mark: bool
    is_elastomer_mark: bool
