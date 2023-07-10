from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Union

from app.schemas.species import Species
from app.models.species import Specie
from app.crud.species import get_specie_by_name, create_specie

from app.api.deps import PermissonsChecker, get_db

router: APIRouter = APIRouter()

#Create specie
@router.post(
    path="/api/species",
    response_model=Species,
    status_code=status.HTTP_201_CREATED,
    tags=["Species"],
    summary="Create a specie",
)
async def create_a_new_specie(
    new_specie: Species,
    db: Session = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> Union[Species, HTTPException]:
    db_specie = await get_specie_by_name(db, new_specie.scientific_name)
    if db_specie:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Specie already exists",
        )
    return await create_specie(db, new_specie)
