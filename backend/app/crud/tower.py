from sqlalchemy.orm import Session
from typing import List, Union
from fastapi import HTTPException

from app.schemas.towers import (
    TowerBase,
    TowerResponse,
    ClearFloraBase,
    ClearFloraResponse,
    ClearHerpetoFaunaBase,
    ClearHerpetoFaunaResponse,
    ClearMammalBase,
    ClearMammalResponse
)

from app.models.towers import (
    Tower,
    Clear_flora,
    Clear_herpetofauna,
    Clear_mammals
)

# Purpuse: CRUD operations for towers

"""
CRUD FOR  TOWERS
"""

# Get if tower exists by number
def get_tower_by_number(db: Session, number: int) -> Union[TowerBase, None]:
    tower = db.query(Tower).filter(Tower.number == number).first()
    return tower

# Get tower by number
def get_tower(db: Session, number: int) -> Union[TowerResponse, None]:
    tower = db.query(Tower).filter(Tower.number == number).first()
    if not tower:
        raise HTTPException(status_code=404, detail="Tower not found")
    return tower

# Get all towers
def get_towers(db: Session) -> List[Tower]:
    return db.query(Tower).all()

# Create tower
def create_tower(db: Session, tower: TowerBase) -> Tower:
    db_tower = Tower(
        number=tower.number,
        latitude=tower.latitude,
        longitude=tower.longitude
    )
    db.add(db_tower)
    db.commit()
    db.refresh(db_tower)
    return db_tower

