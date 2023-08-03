from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Union
from fastapi.responses import JSONResponse
import pandas as pd
from datetime import datetime

from app.api.deps import PermissonsChecker, get_db
from app.crud.rescue_flora import create_plant_nursery
from app.schemas.rescue_flora import PlantNurseryBase

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
            # Start a transaction
            db.begin()

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

            # Commit the transaction
            db.commit()

        except Exception as e:
            # Rollback the transaction in case of an error
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error: {e}",
            )
        finally:
            # Close the database session
            db.close()

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Plant nursery excel file uploaded successfully"},
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an excel file",
        )







