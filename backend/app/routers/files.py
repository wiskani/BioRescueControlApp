from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Union
from fastapi.responses import JSONResponse
import pandas as pd

from app.api.deps import PermissonsChecker, get_db
from app.crud.rescue_flora import create_plant_nursery, create_flora_relocation
from app.schemas.rescue_flora import PlantNurseryBase, FloraRelocationBase

router = APIRouter()

@router.post(
    path="/upload/plant_nursery",
    summary="Upload plant nursery excel file",
    tags=["Upload"],
)
async def upload_plant_nursery(
    file: UploadFile=File(...),
    db: Session = Depends(get_db),
    permissions: str = Depends(PermissonsChecker(["admin"])),
):
    if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
        df = pd.read_excel(file.file)

        # Replace NaN with None
        df = df.where(pd.notna(df), None)

        # Convert date columns to datetime objects
        date_columns = ['entry_date', 'flowering_date', 'departure_date']
        for col in date_columns:
            df[col] = pd.to_datetime(df[col])

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
                    rescue_zone_id=row['rescue_zone_id'],
                    flora_rescue_id=row['flora_rescue_id'],
                    specie_id=row['specie_id'],
                    relocation_zone_id=row['relocation_zone_id'],
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

@router.post(
    path="/upload/flora_relocation",
    summary="Upload flora relocation excel file",
    tags=["Upload"],
)
async def upload_flora_relocation(
    file: UploadFile=File(...),
    db: Session = Depends(get_db),
    permissions: str = Depends(PermissonsChecker(["admin"])),
):
    if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
        df = pd.read_excel(file.file)

        # Replace NaN with None
        df = df.where(pd.notna(df), None)

        # Convert date columns to datetime objects
        date_columns = ['relocation_date' ]
        for col in date_columns:
            df[col] = pd.to_datetime(df[col])

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
                    bryophyte_position=row['bryophyte_position'],
                    bark_type=row['bark_type'],
                    infested_lianas=row['infested_lianas'],
                    relocation_number=row['relocation_number'],
                    other_observations=row['other_observations'],
                    rescue_zone_id=row['rescue_zone_id'],
                    flora_rescue_id=row['flora_rescue_id'],
                    specie_bryophyte_id=row['specie_bryophyte_id'],
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
    








