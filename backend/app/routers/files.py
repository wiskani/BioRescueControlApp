from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status, Router
from sqlalchemy.orm import Session
from typing import List, Union
from fastapi.responses import JSONResponse
import pandas as pd
from datetime import datetime

from app.api.deps import PermissonsChecker, get_db
from app.crud.rescue_flora import create_plant_nursery
from app.schemas.rescue_flora import PlantNurseryBase

router: Router = APIRouter()


#upload plant nursery excel file
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
        #replace null if cell is empty
        df = df.fillna('null')

        for _, row in df.iterrows():
            try:
                new_plant_nursery = PlantNurseryBase(
                    epiphyte_number=row['epiphyte_number'],
                    rescue_date=datetime(row['rescue_date']),
                    rescue_area_latitude=row['rescue_area_latitude'],
                    rescue_area_longitude=row['rescue_area_longitude'],
                    substrate=row['substrate'],


