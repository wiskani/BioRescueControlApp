from sqlalchemy.orm import Session
from typing import List, Union, Optional, Dict, Any
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

#Get tower id by number
async def get_tower_id_by_number(db: Session, number: int) ->Optional[ int]:
    tower_db=db.query(Tower).filter(Tower.number == number).first()
    if tower_db is not None:
        return tower_db.id
    else:
        return None

# Get if tower exists by number
async def get_tower_by_number(db: Session, number: int) -> Union[TowerResponse, None]:
    return db.query(Tower).filter(Tower.number == number).first()

# Get all towers
async def get_towers(db: Session) -> List[Tower]:
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
async def delete_tower(db: Session, tower_id: int) -> Tower :
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
async def get_clear_flora_by_tower_number(db: Session, number: int) -> Union[ClearFloraResponse, None]:
    tower_id = await get_tower_id_by_number(db, number)
    return db.query(Clear_flora).filter(Clear_flora.tower_id == tower_id).first()

#Get clear_flora_id by tower number
async def get_clear_flora_id_by_tower_number(db: Session, number: int) ->Optional[ int]:
    tower_id = await get_tower_id_by_number(db, number)
    clear_flora_db=db.query(Clear_flora).filter(Clear_flora.tower_id == tower_id).first()
    if clear_flora_db is not None:
        return clear_flora_db.id
    else:
        return None

# Get all clear flora
async def get_clear_flora(db: Session) -> List[Clear_flora]:
    return db.query(Clear_flora).all()

# Create clear flora
async def create_clear_flora(db: Session, clear_flora: ClearFloraBase, tower_number:int) -> Clear_flora | HTTPException:
    towerid = await get_tower_id_by_number(db, tower_number)
    if towerid is None:
        raise HTTPException(status_code=404, detail="Tower not found")
    else:
        if await get_clear_flora_by_tower_number(db, tower_number) is not None:
            raise HTTPException(status_code=404, detail="Clear flora already exists for this tower")
        else:
            db_clear_flora = Clear_flora(
                is_clear=clear_flora.is_clear,
                tower_id= towerid,
                clear_at=clear_flora.clear_at,
            )
            db.add(db_clear_flora)
            db.commit()
            db.refresh(db_clear_flora)
            return db_clear_flora

# Update clear flora
async def update_clear_flora(db: Session,  clear_flora: ClearFloraBase, tower_number:int) -> ClearFloraResponse | HTTPException:
    db_clear_flora = await get_clear_flora_by_tower_number(db, tower_number)
    if not db_clear_flora:
        raise HTTPException(status_code=404, detail="Clear flora not found")
    tower_id = await get_tower_id_by_number(db, tower_number)
    if tower_id is None:
        raise HTTPException(status_code=404, detail="Tower not found")
    db_clear_flora.is_clear = clear_flora.is_clear
    db_clear_flora.tower_id = tower_id
    db_clear_flora.clear_at = clear_flora.clear_at
    db.commit()
    db.refresh(db_clear_flora)
    return db_clear_flora

# Delete clear flora
async def delete_clear_flora(db: Session, tower_number: int) -> Dict[str, str] | HTTPException :
    db_clear_flora = await get_clear_flora_by_tower_number(db, tower_number) 
    if not db_clear_flora:
        raise HTTPException(status_code=404, detail="Clear flora not found")
    try:
        db.delete(db_clear_flora)
        db.commit()
        return {"message": "Clear flora deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


"""
CRUD FOR CLEAR HERPETOFAUNA
"""
# Get if clear herpetofauna existis by tower number
async def get_clear_herpetofauna_by_tower_number(db: Session, number: int) -> Union[ClearHerpetoFaunaResponse, None]:
    tower_id = await get_tower_id_by_number(db, number)
    return db.query(Clear_herpetofauna).filter(Clear_herpetofauna.tower_id == tower_id).first()

#Get clear_herpetofauna_id by tower number
async def get_clear_herpetofauna_id_by_tower_number(db: Session, number: int) ->Optional[ int]:
    tower_id = await get_tower_id_by_number(db, number)
    clear_herpetofauna_db=db.query(Clear_herpetofauna).filter(Clear_herpetofauna.tower_id == tower_id).first()
    if clear_herpetofauna_db is not None:
        return clear_herpetofauna_db.id
    else:
        return None

# Get all clear herpetofauna
async def get_clear_herpetofauna(db: Session) -> List[Clear_herpetofauna]:
    return db.query(Clear_herpetofauna).all()

# Create clear herpetofauna
async def create_clear_herpetofauna(db: Session, clear_herpetofauna: ClearHerpetoFaunaBase, tower_number:int) -> Clear_herpetofauna | HTTPException:
    towerid = await get_tower_id_by_number(db, tower_number)
    if towerid is None:
        raise HTTPException(status_code=404, detail="Tower not found")
    else:
        if await get_clear_herpetofauna_by_tower_number(db, tower_number) is not None:
            raise HTTPException(status_code=404, detail="Clear herpetofauna already exists for this tower")
        else:
            db_clear_herpetofauna = Clear_herpetofauna(
                is_clear=clear_herpetofauna.is_clear,
                tower_id= towerid,
                clear_at=clear_herpetofauna.clear_at,
            )
            db.add(db_clear_herpetofauna)
            db.commit()
            db.refresh(db_clear_herpetofauna)
            return db_clear_herpetofauna

# Update clear herpetofauna
async def update_clear_herpetofauna(db: Session,  clear_herpetofauna: ClearHerpetoFaunaBase, tower_number:int) -> ClearHerpetoFaunaResponse | HTTPException:
    db_clear_herpetofauna = await get_clear_herpetofauna_by_tower_number(db, tower_number)
    if not db_clear_herpetofauna:
        raise HTTPException(status_code=404, detail="Clear herpetofauna not found")
    tower_id = await get_tower_id_by_number(db, tower_number)
    if tower_id is None:
        raise HTTPException(status_code=404, detail="Tower not found")
    db_clear_herpetofauna.is_clear = clear_herpetofauna.is_clear
    db_clear_herpetofauna.tower_id = tower_id
    db_clear_herpetofauna.clear_at = clear_herpetofauna.clear_at
    db.commit()
    db.refresh(db_clear_herpetofauna)
    return db_clear_herpetofauna

# Delete clear herpetofauna
async def delete_clear_herpetofauna(db: Session, tower_number: int) -> Dict[str, str] | HTTPException :
    db_clear_herpetofauna = await get_clear_herpetofauna_by_tower_number(db, tower_number) 
    if not db_clear_herpetofauna:
        raise HTTPException(status_code=404, detail="Clear herpetofauna not found")
    try:
        db.delete(db_clear_herpetofauna)
        db.commit()
        return {"message": "Clear herpetofauna deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


"""
CRUD FOR CLEAR MAMMAL
"""
# Get if clear mammal existis by tower number
async def get_clear_mammal_by_tower_number(db: Session, number: int) -> Union[ClearMammalResponse, None]:
    tower_id = await get_tower_id_by_number(db, number)
    return db.query(Clear_mammals).filter(Clear_mammals.tower_id == tower_id).first()

#Get clear_mammal_id by tower number
async def get_clear_mammal_id_by_tower_number(db: Session, number: int) ->Optional[ int]:
    tower_id = await get_tower_id_by_number(db, number)
    clear_mammal_db=db.query(Clear_mammals).filter(Clear_mammals.tower_id == tower_id).first()
    if clear_mammal_db is not None:
        return clear_mammal_db.id
    else:
        return None

# Get all clear mammal
async def get_clear_mammal(db: Session) -> List[Clear_mammals]:
    return db.query(Clear_mammals).all()

# Create clear mammal
async def create_clear_mammal(db: Session, clear_mammal: ClearMammalBase, tower_number:int) -> Clear_mammals | HTTPException:
    towerid = await get_tower_id_by_number(db, tower_number)
    if towerid is None:
        raise HTTPException(status_code=404, detail="Tower not found")
    else:
        if await get_clear_mammal_by_tower_number(db, tower_number) is not None:
            raise HTTPException(status_code=404, detail="Clear mammal already exists for this tower")
        else:
            db_clear_mammal = Clear_mammals(
                is_clear=clear_mammal.is_clear,
                tower_id= towerid,
                clear_at=clear_mammal.clear_at,
            )
            db.add(db_clear_mammal)
            db.commit()
            db.refresh(db_clear_mammal)
            return db_clear_mammal

# Update clear mammal
async def update_clear_mammal(db: Session,  clear_mammal: ClearMammalBase, tower_number:int) -> ClearMammalResponse | HTTPException:
    db_clear_mammal = await get_clear_mammal_by_tower_number(db, tower_number)
    if not db_clear_mammal:
        raise HTTPException(status_code=404, detail="Clear mammal not found")
    tower_id = await get_tower_id_by_number(db, tower_number)
    if tower_id is None:
        raise HTTPException(status_code=404, detail="Tower not found")
    db_clear_mammal.is_clear = clear_mammal.is_clear
    db_clear_mammal.tower_id = tower_id
    db_clear_mammal.clear_at = clear_mammal.clear_at
    db.commit()
    db.refresh(db_clear_mammal)
    return db_clear_mammal

# Delete clear mammal
async def delete_clear_mammal(db: Session, tower_number: int) -> Dict[str, str] | HTTPException :
    db_clear_mammal = await get_clear_mammal_by_tower_number(db, tower_number) 
    if not db_clear_mammal:
        raise HTTPException(status_code=404, detail="Clear mammal not found")
    try:
        db.delete(db_clear_mammal)
        db.commit()
        return {"message": "Clear mammal deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


