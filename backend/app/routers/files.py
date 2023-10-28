from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Union
from fastapi.responses import JSONResponse
import pandas as pd

from app.api.deps import PermissonsChecker, get_db

#CRUD
from app.crud.rescue_flora import create_plant_nursery, create_flora_relocation
from app.crud.tower import create_tower, get_tower_by_number
from app.crud.rescue_herpetofauna import(
    create_transect_herpetofauna,
    get_transect_herpetofauna_by_number,
    create_rescue_herpetofauna,
    get_rescue_herpetofauna_by_number,
    create_mark_herpetofauna,
    get_mark_herpetofauna_by_number
)

#Schemas
from app.schemas.rescue_flora import PlantNurseryBase, FloraRelocationBase
from app.schemas.rescue_herpetofauna import TransectHerpetofaunaCreate, RescueHerpetofaunaCreate, MarkHerpetofaunaCreate
from app.schemas.towers import TowerBase
from app.schemas.services import UTMData

from app.services.files import (
    convert_to_datetime,
    remplace_nan_with_none,
    none_value,
    insertGEOData,
    addIdSpecieByName,
    addBooleanByGender,
    addMarkIdByNumber,
    addAgeGroupIdByName
)

router = APIRouter()

# Upload plant nursery excel file
@router.post(
    path="/upload/plant_nursery",
    response_model= None,
    summary="Upload plant nursery excel file",
    tags=["Upload"],
)
async def upload_plant_nursery(
    file: UploadFile=File(...),
    db: AsyncSession = Depends(get_db),
    permissions: str = Depends(PermissonsChecker(["admin"])),
):
    if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
        df = pd.read_excel(file.file)

        # Replace NaN with None
        df = df.where(pd.notna(df), None)

        # Convert date columns to datetime objects
        date_columns = ['entry_date', 'flowering_date', 'departure_date']
        df = convert_to_datetime(df, date_columns)

        try:
            for _, row in df.iterrows():
                new_plant_nursery = PlantNurseryBase(
                    entry_date=row['entry_date'],
                    cod_reg=row['cod_reg'],
                    health_status_epiphyte=row['health_status_epiphyte'],
                    vegetative_state=row['vegetative_state'],
                    flowering_date=row['flowering_date'],
                    treatment_product=row['treatment_product'],
                    is_pruned=row['is_pruned'],
                    is_phytosanitary_treatment=row['is_phytosanitary_treatment'],
                    substrate=row['substrate'],
                    departure_date=row['departure_date'],
                    flora_rescue_id=row['flora_rescue_id'],
                )
                await create_plant_nursery(db, new_plant_nursery)
        except Exception as e:
            # Rollback the transaction in case of an error
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error: {e}",
            )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Plant nursery excel file uploaded successfully"},
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an excel file",
        )

# Upload flora relocation excel file
@router.post(
    path="/upload/flora_relocation",
    response_model= None,
    summary="Upload flora relocation excel file",
    tags=["Upload"],
)
async def upload_flora_relocation(
    file: UploadFile=File(...),
    db: AsyncSession = Depends(get_db),
    permissions: str = Depends(PermissonsChecker(["admin"])),
):
    if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
        df = pd.read_excel(file.file)

        # Replace NaN with None
        df = df.fillna('None')

        # chek if NaN is in df 
        if df.isnull().values.any():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must not contain NaN",
            )

        #fuction to return None value if value is 'None'
        def none_value(value):
            if value == 'None':
                return None
            else:
                return value

        # Convert date columns to datetime objects
        date_columns = ['relocation_date' ]
        df = convert_to_datetime(df, date_columns)

        try:
            for _, row in df.iterrows():
                new_flora_relocation = FloraRelocationBase(
                    relocation_date=row['relocation_date'],
                    size=row['size'],
                    epiphyte_phenology=row['epiphyte_phenology'],
                    johanson_zone=row['johanson_zone'],
                    relocation_position_latitude=row['relocation_position_latitude'],
                    relocation_position_longitude=row['relocation_position_longitude'],
                    bryophyte_number=row['bryophyte_number'],
                    dap_bryophyte=row['dap_bryophyte'],
                    height_bryophyte=row['height_bryophyte'],
                    bark_type=row['bark_type'],
                    infested_lianas=row['infested_lianas'],
                    relocation_number=row['relocation_number'],
                    other_observations=none_value(row['other_observations']),
                    flora_rescue_id=row['flora_rescue_id'],
                    specie_bryophyte_id=none_value(row['specie_bryophyte_id']),
                    genus_bryophyte_id=none_value(row['genus_bryophyte_id']),
                    family_bryophyte_id=none_value(row['family_bryophyte_id']),
                    relocation_zone_id=row['relocation_zone_id'],
                )
                await create_flora_relocation(db, new_flora_relocation)
        except Exception as e:
            # Rollback the transaction in case of an error
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error: {e}",
            )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Flora relocation excel file uploaded successfully"},
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an excel file",
        )

#upload tower excel file
@router.post(
    path="/upload/tower",
    response_model= None,
    summary="Upload tower excel file",
    tags=["Upload"],
)
async def upload_tower(
    file: UploadFile=File(...),
    db: AsyncSession = Depends(get_db),
    permissions: str = Depends(PermissonsChecker(["admin"])),
):
    if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
        df = pd.read_excel(file.file)

        # Replace NaN with None
        df = remplace_nan_with_none(df)

        numberExistList = []

        for _, row in df.iterrows():
            try:
                new_tower = TowerBase(
                    number=row['number'],
                    latitude=row['lat'],
                    longitude=row['lon'],
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Error to create tower data: {e}",
                )
            if await get_tower_by_number(db, new_tower.number):
                numberExistList.append(new_tower.number)
                continue
            else:
                await create_tower(db, new_tower)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Tower excel file uploaded successfully", "numberExistList": numberExistList},
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an excel file",
        )


# Upload transect herpetofauna excel file
@router.post(
    path="/upload/transect_herpetofauna",
    summary="Upload transect herpetofauna excel file",
    response_model= None,
    tags=["Upload"],
)
async def upload_transect_herpetofauna(
    file: UploadFile=File(...),
    db: AsyncSession = Depends(get_db),
    permissions: str = Depends(PermissonsChecker(["admin"])),
) -> JSONResponse | HTTPException:
    if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
        df = pd.read_excel(file.file)

        # Replace NaN with None
        df = remplace_nan_with_none(df)

        # Convert date columns to datetime objects
        date_columns = [
            'date_in',
            'date_out',
        ]
        UTM_columns_in = {
            'easting': 'este_in',
            'northing': 'sur_in',
            'zone_number': 'zona',
            'zone_letter': 'zona_letra',
        }
        UTM_columns_out = {
            'easting': 'este_out',
            'northing': 'sur_out',
            'zone_number': 'zona',
            'zone_letter': 'zona_letra',
        }

        #Names of columns geodata columns to in transect
        nameLatitude_in = 'latitude_in'
        nameLongitude_in = 'longitude_in'

        #Names of columns geodata columns to out transect
        nameLatitude_out = 'latitude_out'
        nameLongitude_out = 'longitude_out'

        # Insert columns lat y lon to df
        df = insertGEOData(df, UTM_columns_in, nameLatitude_in, nameLongitude_in)
        df = insertGEOData(df, UTM_columns_out, nameLatitude_out, nameLongitude_out)

        # Cnvert time to datetime
        df = convert_to_datetime(df, date_columns)

        numberExistList = []

        for _, row in df.iterrows():
            try:
                new_transect_herpetofauna = TransectHerpetofaunaCreate(
                    number=row['num'],
                    date_in=row['date_in'],
                    date_out=row['date_out'],
                    latitude_in=row['latitude_in'],
                    longitude_in=row['longitude_in'],
                    altitude_in=row['altitud_in'],
                    latitude_out=row['latitude_out'],
                    longitude_out=row['longitude_out'],
                    altitude_out=row['altitud_out'],
                    tower_id=row['torre'],
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Error: {e}",
                )
            if await get_transect_herpetofauna_by_number(db, new_transect_herpetofauna.number):
                numberExistList.append(new_transect_herpetofauna.number)
                continue
            else:
                await  create_transect_herpetofauna(db, new_transect_herpetofauna)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Flora relocation excel file uploaded successfully", "Not upload numbers because repeate": numberExistList},
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an excel file",
        )

# Upload rescue herpetofauna excel file
@router.post(
    path="/upload/rescue_herpetofauna",
    summary="Upload rescue herpetofauna excel file",
    response_model= None,
    tags=["Upload"],
)
async def upload_rescue_herpetofauna(
    file: UploadFile=File(...),
    db: AsyncSession = Depends(get_db),
    permissions: str = Depends(PermissonsChecker(["admin"])),
) -> JSONResponse | HTTPException:
    if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
        df = pd.read_excel(file.file)

        # Replace NaN with None
        df = remplace_nan_with_none(df)

        df, specieListWithOutName = await addIdSpecieByName(db, df, "especie")
        df, genderListWithOutName = await addBooleanByGender(db, df, "genero",("Macho", "Hembra"))
        df, markListWithOutName = await addMarkIdByNumber(db, df, "codigo_marcaje")
        df, ageGroupListWithOutName = await addAgeGroupIdByName(db, df, "clase_etaria")

        numberExistList = []

        for _, row in df.iterrows():
            try:
                new_rescue_herpetofauna = RescueHerpetofaunaCreate(
                    number=row['num'],
                    gender=row['booleanGender'],
                    specie_id=row['idSpecie'],
                    mark_herpetofauna_id=row['idMark'],
                    transect_herpetofauna_id=row['num_t'],
                    age_group_id=row['idAgeGroup'],
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Error: {e}",
                )
            if await get_rescue_herpetofauna_by_number(db, new_rescue_herpetofauna.number):
                numberExistList.append(new_rescue_herpetofauna.number)
                continue
            else:
                await create_rescue_herpetofauna (db, new_rescue_herpetofauna)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Flora relocation excel file uploaded successfully",
                "Not upload numbers because repeate": numberExistList,
                "Some species not found": specieListWithOutName,
                "Some gender not found or are null": genderListWithOutName,
                "Some mark not found or are null": markListWithOutName,
                "Some age group not found or are null": ageGroupListWithOutName,
                },
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an excel file",
        )

# Upload mark herpetofauna excel file
@router.post(
    path="/upload/mark_herpetofauna",
    summary="Upload mark herpetofauna excel file",
    response_model= None,
    tags=["Upload"],
)
async def upload_mark_herpetofauna(
    file: UploadFile=File(...),
    db: AsyncSession = Depends(get_db),
    permissions: str = Depends(PermissonsChecker(["admin"])),
) -> JSONResponse | HTTPException:
    if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
        df = pd.read_excel(file.file)

        # Replace NaN with None
        df = remplace_nan_with_none(df)

        # Convert date columns to datetime objects
        date_columns = [
            'date',
        ]
        df = convert_to_datetime(df, date_columns)

        numberExistList = []

        for _, row in df.iterrows():
            try:
                new_mark_herpetofauna = MarkHerpetofaunaCreate(
                    date=row['date'],
                    number=row['num'],
                    code=row['code'],
                    LHC=row['LHC'],
                    weight=row['weight'],
                    is_photo_mark=row['is_photo_mark'],
                    is_elastomer_mark=row['is_elastomer_mark'],
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Error: {e}",
                )
            if await get_mark_herpetofauna_by_number(db, new_mark_herpetofauna.number):
                numberExistList.append(new_mark_herpetofauna.number)
                continue
            else:
                await create_mark_herpetofauna(db, new_mark_herpetofauna)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Flora relocation excel file uploaded successfully", "Not upload numbers because repeate": numberExistList},
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an excel file",
        )







