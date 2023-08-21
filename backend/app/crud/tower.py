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
async def get_tower_by_number(db: Session, number: int) -> Union[TowerBase, None]:
    return db.query(Tower).filter(Tower.number == number).first()

# Get all towers
async def get_towers(db: Session) -> List[TowerResponse]:
    return db.query(Tower).all()

# Create tower
async def create_tower(db: Session, tower: TowerBase) -> TowerResponse:
    db_tower = Tower(
        number=tower.number,
        latitude=tower.latitude,
        longitude=tower.longitude
    )
    db.add(db_tower)
    db.commit()
    db.refresh(db_tower)
    return db_tower

# Update tower
async def update_tower(db: Session, tower_id: int, tower: TowerBase) -> Tower:
    db_tower = db.query(Tower).filter(Tower.id == tower_id  ).first()
    if not db_tower:
        raise HTTPException(status_code=404, detail="Tower not found")
    db_tower.number = tower.number
    db_tower.latitude = tower.latitude
    db_tower.longitude = tower.longitude
    db.commit()
    db.refresh(db_tower)
    return db_tower

# Delete tower
def delete_tower(db: Session, tower_id: int) -> Tower:
    db_tower = db.query(Tower).filter(Tower.id == tower_id ).first()
    if not db_tower:
        raise HTTPException(status_code=404, detail="Tower not found")
    db.delete(db_tower)
    db.commit()
    return db_tower

"""
CRUD FOR CLEAR FLORA
"""
# Get if clear flora existis by tower number
async def get_clear_flora_by_tower_number(db: Session, number: int) -> Union[ClearFloraBase, None]:
    return db.query(Clear_flora).filter(Clear_flora.tower_number == number).first()

# Get all clear flora
async def get_clear_flora(db: Session) -> List[Clear_flora]:
    return db.query(Clear_flora).all()

# Create clear flora
async def create_clear_flora(db: Session, clear_flora: ClearFloraBase) -> Clear_flora:
    db_clear_flora = Clear_flora(
        is_clear=clear_flora.is_clear,
        tower_id=clear_flora.tower_id,
        clear_at=clear_flora.clear_at,
    )
    db.add(db_clear_flora)
    db.commit()
    db.refresh(db_clear_flora)
    return db_clear_flora

# Update clear flora
async def update_clear_flora(db: Session, clear_flora_id: int, clear_flora: ClearFloraBase) -> Clear_flora:
    db_clear_flora = db.query(Clear_flora).filter(Clear_flora.id == clear_flora_id).first()
    if not db_clear_flora:
        raise HTTPException(status_code=404, detail="Clear flora not found")
    db_clear_flora.is_clear = clear_flora.is_clear
    db_clear_flora.tower_id = clear_flora.tower_id
    db_clear_flora.clear_at = clear_flora.clear_at
    db.commit()
    db.refresh(db_clear_flora)
    return db_clear_flora

# Delete clear flora
async def delete_clear_flora(db: Session, clear_flora_id: int) -> Clear_flora:
    db_clear_flora = db.query(Clear_flora).filter(Clear_flora.id == clear_flora_id).first()
    if not db_clear_flora:
        raise HTTPException(status_code=404, detail="Clear flora not found")
    db.delete(db_clear_flora)
    db.commit()
    return db_clear_flora

"""
CRUD FOR CLEAR HERPETOFAUNA
"""
# Get if clear herpetofauna existis by tower number
async def get_clear_herpetofauna_by_tower_number(db: Session, number: int) -> Union[ClearHerpetoFaunaBase, None]:
    return db.query(Clear_herpetofauna).filter(Clear_herpetofauna.tower_number == number).first()

# Get all clear herpetofauna
async def get_clear_herpetofauna(db: Session) -> List[Clear_herpetofauna]:
    return db.query(Clear_herpetofauna).all()

# Create clear herpetofauna
async def create_clear_herpetofauna(db: Session, clear_herpetofauna: ClearHerpetoFaunaBase) -> Clear_herpetofauna:
    db_clear_herpetofauna = Clear_herpetofauna(
        is_clear=clear_herpetofauna.is_clear,
        tower_id=clear_herpetofauna.tower_id,
        clear_at=clear_herpetofauna.clear_at,
    )
    db.add(db_clear_herpetofauna)
    db.commit()
    db.refresh(db_clear_herpetofauna)
    return db_clear_herpetofauna

# Update clear herpetofauna
async def update_clear_herpetofauna(db: Session, clear_herpetofauna_id: int, clear_herpetofauna: ClearHerpetoFaunaBase) -> Clear_herpetofauna:
    db_clear_herpetofauna = db.query(Clear_herpetofauna).filter(Clear_herpetofauna.id == clear_herpetofauna_id).first()
    if not db_clear_herpetofauna:
        raise HTTPException(status_code=404, detail="Clear herpetofauna not found")
    db_clear_herpetofauna.is_clear = clear_herpetofauna.is_clear
    db_clear_herpetofauna.tower_id = clear_herpetofauna.tower_id
    db_clear_herpetofauna.clear_at = clear_herpetofauna.clear_at
    db.commit()
    db.refresh(db_clear_herpetofauna)
    return db_clear_herpetofauna

# Delete clear herpetofauna
async def delete_clear_herpetofauna(db: Session, clear_herpetofauna_id: int) -> Clear_herpetofauna:
    db_clear_herpetofauna = db.query(Clear_herpetofauna).filter(Clear_herpetofauna.id == clear_herpetofauna_id).first()
    if not db_clear_herpetofauna:
        raise HTTPException(status_code=404, detail="Clear herpetofauna not found")
    db.delete(db_clear_herpetofauna)
    db.commit()
    return db_clear_herpetofauna

"""
CRUD FOR CLEAR MAMMAL
"""
# Get if clear mammal existis by tower number
async def get_clear_mammal_by_tower_number(db: Session, number: int) -> Union[ClearMammalBase, None]:
    return db.query(Clear_mammals).filter(Clear_mammals.tower_number == number).first()

# Get all clear mammal
async def get_clear_mammal(db: Session) -> List[Clear_mammals]:
    return db.query(Clear_mammals).all()

# Create clear mammal
async def create_clear_mammal(db: Session, clear_mammal: ClearMammalBase) -> Clear_mammals:
    db_clear_mammal = Clear_mammals(
        is_clear=clear_mammal.is_clear,
        tower_id=clear_mammal.tower_id,
        clear_at=clear_mammal.clear_at,
    )
    db.add(db_clear_mammal)
    db.commit()
    db.refresh(db_clear_mammal)
    return db_clear_mammal

# Update clear mammal
async def update_clear_mammal(db: Session, clear_mammal_id: int, clear_mammal: ClearMammalBase) -> Clear_mammals:
    db_clear_mammal = db.query(Clear_mammals).filter(Clear_mammals.id == clear_mammal_id).first()
    if not db_clear_mammal:
        raise HTTPException(status_code=404, detail="Clear mammal not found")
    db_clear_mammal.is_clear = clear_mammal.is_clear
    db_clear_mammal.tower_id = clear_mammal.tower_id
    db_clear_mammal.clear_at = clear_mammal.clear_at
    db.commit()
    db.refresh(db_clear_mammal)
    return db_clear_mammal

# Delete clear mammal
async def delete_clear_mammal(db: Session, clear_mammal_id: int) -> Clear_mammals:
    db_clear_mammal = db.query(Clear_mammals).filter(Clear_mammals.id == clear_mammal_id).first()
    if not db_clear_mammal:
        raise HTTPException(status_code=404, detail="Clear mammal not found")
    db.delete(db_clear_mammal)
    db.commit()
    return db_clear_mammal



