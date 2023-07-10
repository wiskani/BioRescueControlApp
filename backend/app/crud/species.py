from sqlalchemy.orm import Session
from typing import List, Union
from fastapi import HTTPException

from app.schemas.species import Species
from app.models.species import Specie

#Purpose: CRUD operations for Species

#Get if specie exists
async def get_specie_by_name(db: Session, scientific_name: str) -> Union[Specie, None]:
    return db.query(Specie).filter(Specie.scientific_name == scientific_name).first()

#Create a specie
async def create_specie(db: Session, specie: Species) -> Specie:
    db_specie = Specie(
        scientific_name = specie.scientific_name,
        common_name = specie.common_name
    )
    db.add(db_specie)
    db.commit()
    db.refresh(db_specie)
    return db_specie
