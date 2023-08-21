from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Union, Dict

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

from app.crud.tower import (

    #tower
    get_tower_by_number,
    get_towers,
    create_tower,
    update_tower,
    delete_tower,

    #clear_flora
    get_clear_flora_by_tower_number,
    get_clear_flora,
    create_clear_flora,
    update_clear_flora,
    delete_clear_flora,

    #clear_herpetofauna
    get_clear_herpetofauna_by_tower_number,
    get_clear_herpetofauna,
    create_clear_herpetofauna,
    update_clear_herpetofauna,
    delete_clear_herpetofauna,

    #clear_mammals
    get_clear_mammal_by_tower_number,
    get_clear_mammal,
    create_clear_mammal,
    update_clear_mammal,
    delete_clear_mammal
)

from app.api.deps import PermissonsChecker, get_db

router:APIRouter = APIRouter()


"""
CRUD FOR  TOWERS
"""

# Create tower
@router.post(
    path="/api/towers",
    response_model=TowerResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["towers"],
    summary="Create tower",
)
async def create_tower_api(
    tower: TowerBase,
    db: Session = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"])),
) -> TowerResponse:
    db_tower = await get_tower_by_number(db, tower.number)
    if db_tower:
        raise HTTPException(status_code=400, detail="Tower already registered")
    return await create_tower(db, tower)

# Get all towers
@router.get(
    path="/api/towers",
    response_model=List[TowerResponse],
    tags=["towers"],
    summary="Get all towers",
)
async def get_towers_api(
    db: Session = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin", "user"])),
) -> List[TowerResponse]:
    return await get_towers(db)

# Get tower by number
@router.get(
    path="/api/towers/{number}",
    response_model=TowerResponse,
    tags=["towers"],
    summary="Get tower by number",
)
async def get_tower_by_number_api(
    number: int,
    db: Session = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin", "user"])),
) -> Union[TowerResponse, None]:
    return await get_tower_by_number(db, number)

# Update tower
@router.put(
    path="/api/towers/{tower_id}",
    response_model=TowerResponse,
    tags=["towers"],
    summary="Update tower",
)
async def update_tower_api(
    tower_id: int,
    tower: TowerBase,
    db: Session = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"])),
) -> TowerResponse:
    return await update_tower(db, tower_id, tower)

# Delete tower
@router.delete(
    path="/api/towers/{tower_id}",
    response_model=TowerResponse,
    tags=["towers"],
    summary="Delete tower",
)
async def delete_tower_api(
    tower_id: int,
    db: Session = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"])),
) -> TowerResponse:
    return await delete_tower(db, tower_id)





)
