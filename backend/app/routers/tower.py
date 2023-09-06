from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Union, Dict
from pydantic import parse_obj_as

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

from app.models.towers import Tower, Clear_flora, Clear_herpetofauna, Clear_mammals

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
    autorized: bool = Depends(PermissonsChecker(["admin"])),
) -> List[TowerResponse]:
    towers: List[Tower]= await get_towers(db)
    return parse_obj_as(List[TowerResponse], towers)

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
) -> Dict:
     await delete_tower(db, tower_id)
     return {"message": "Tower deleted successfully"}

"""
CRUD FOR CLEAR FLORA
"""

# Create clear flora
@router.post(
    path="/api/clear_flora/{tower_number}",
    response_model=ClearFloraResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["clear_flora"],
    summary="Create clear flora",
)
async def create_clear_flora_api(
    tower_number: int,
    clear_flora: ClearFloraBase,
    db: Session = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"])),
) -> ClearFloraResponse | HTTPException:
    return await create_clear_flora(db, clear_flora, tower_number)

# Get all clear flora
@router.get(
    path="/api/clear_flora",
    response_model=List[ClearFloraResponse],
    tags=["clear_flora"],
    summary="Get all clear flora",
)
async def get_clear_flora_api(
    db: Session = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"])),
) -> List[ClearFloraResponse]:
    clear_flora: List[Clear_flora]= await get_clear_flora(db)
    return parse_obj_as(List[ClearFloraResponse], clear_flora)

# Get clear flora by tower number
@router.get(
    path="/api/clear_flora/{tower_number}",
    response_model=ClearFloraResponse,
    tags=["clear_flora"],
    summary="Get clear flora by id",
)
async def get_clear_flora_by_tower_number_api(
    tower_number: int,
    db: Session = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin", "user"])),
) -> Union[ClearFloraResponse, None]:
    return await get_clear_flora_by_tower_number(db, tower_number)

# Update clear flora
@router.put(
    path="/api/clear_flora/{tower_number}",
    response_model=ClearFloraResponse,
    tags=["clear_flora"],
    summary="Update clear flora",
)
async def update_clear_flora_api(
    tower_number: int,
    clear_flora: ClearFloraBase,
    db: Session = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"])),
) -> ClearFloraResponse:
    return await update_clear_flora(db, clear_flora,  tower_number )

# Delete clear flora
@router.delete(
    path="/api/clear_flora/{tower_number}",
    tags=["clear_flora"],
    summary="Delete clear flora",
)
async def delete_clear_flora_api(
    tower_number: int,
    db: Session = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"])),
) -> Dict:
    try:
        await delete_clear_flora(db, tower_number)
        return {"message": "Clear flora deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

"""
CRUD FOR CLEAR HERPETOFAUNA
"""

# Create clear herpetofauna
@router.post(
    path="/api/clear_herpetofauna/{tower_number}",
    response_model=ClearHerpetoFaunaResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["clear_herpetofauna"],
    summary="Create clear herpetofauna",
)
async def create_clear_herpetofauna_api(
    tower_number: int,
    clear_herpetofauna: ClearHerpetoFaunaBase,
    db: Session = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"])),
) -> ClearHerpetoFaunaResponse | HTTPException:
    return await create_clear_herpetofauna(db, clear_herpetofauna, tower_number)

# Get all clear herpetofauna
@router.get(
    path="/api/clear_herpetofauna",
    response_model=List[ClearHerpetoFaunaResponse],
    tags=["clear_herpetofauna"],
    summary="Get all clear herpetofauna",
)
async def get_clear_herpetofauna_api(
    db: Session = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"])),
) -> List[ClearHerpetoFaunaResponse]:
    clear_herpetofauna: List[Clear_herpetofauna]= await get_clear_herpetofauna(db)
    return parse_obj_as(List[ClearHerpetoFaunaResponse], clear_herpetofauna)

# Get clear herpetofauna by tower number
@router.get(
    path="/api/clear_herpetofauna/{tower_number}",
    response_model=ClearHerpetoFaunaResponse,
    tags=["clear_herpetofauna"],
    summary="Get clear herpetofauna by id",
)
async def get_clear_herpetofauna_by_tower_number_api(
    tower_number: int,
    db: Session = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin", "user"])),
) -> Union[ClearHerpetoFaunaResponse, None]:
    return await get_clear_herpetofauna_by_tower_number(db, tower_number)




