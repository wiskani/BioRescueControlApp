from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Union, Dict
from pydantic import TypeAdapter

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
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"])),
) -> Tower:
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
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"])),
) -> List[Tower]:
    towers: List[Tower]= await get_towers(db)
    return towers

# Get tower by number
@router.get(
    path="/api/towers/{number}",
    response_model=TowerResponse,
    tags=["towers"],
    summary="Get tower by number",
)
async def get_tower_by_number_api(
    number: int,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin", "user"])),
) -> Tower| None:
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
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"])),
) -> Tower:
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
    db: AsyncSession = Depends(get_db),
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
    db: AsyncSession = Depends(get_db),
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
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"])),
) -> List[Clear_flora]:
    clear_flora: List[Clear_flora]= await get_clear_flora(db)
    return clear_flora

# Get clear flora by tower number
@router.get(
    path="/api/clear_flora/{tower_number}",
    response_model=ClearFloraResponse,
    tags=["clear_flora"],
    summary="Get clear flora by id",
)
async def get_clear_flora_by_tower_number_api(
    tower_number: int,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin", "user"])),
) -> Clear_flora | None:
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
    db: AsyncSession = Depends(get_db),
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
    db: AsyncSession = Depends(get_db),
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
    db: AsyncSession = Depends(get_db),
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
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"])),
) -> List[ClearHerpetoFaunaResponse]:
    clear_herpetofauna: List[Clear_herpetofauna]= await get_clear_herpetofauna(db)
    clear_herpetofuana_response: List[ClearHerpetoFaunaResponse] = []
    for clear in clear_herpetofauna:
        db_clear_herpetofauna = ClearHerpetoFaunaResponse(
                id=clear.id,
                tower_id=clear.tower_id,
                is_clear=clear.is_clear,
                clear_at=clear.clear_at
            )
        clear_herpetofuana_response.append(db_clear_herpetofauna)
    return clear_herpetofuana_response


# Get clear herpetofauna by tower number
@router.get(
    path="/api/clear_herpetofauna/{tower_number}",
    response_model=ClearHerpetoFaunaResponse,
    tags=["clear_herpetofauna"],
    summary="Get clear herpetofauna by id",
)
async def get_clear_herpetofauna_by_tower_number_api(
    tower_number: int,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin", "user"])),
) -> Union[ClearHerpetoFaunaResponse, None]:
    return await get_clear_herpetofauna_by_tower_number(db, tower_number)

# Update clear herpetofauna
@router.put(
    path="/api/clear_herpetofauna/{tower_number}",
    response_model=ClearHerpetoFaunaResponse,
    tags=["clear_herpetofauna"],
    summary="Update clear herpetofauna",
)
async def update_clear_herpetofauna_api(
    tower_number: int,
    clear_herpetofauna: ClearHerpetoFaunaBase,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"])),
) -> ClearHerpetoFaunaResponse:
    return await update_clear_herpetofauna(db, clear_herpetofauna,  tower_number )

# Delete clear herpetofauna
@router.delete(
    path="/api/clear_herpetofauna/{tower_number}",
    tags=["clear_herpetofauna"],
    summary="Delete clear herpetofauna",
)
async def delete_clear_herpetofauna_api(
    tower_number: int,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"])),
) -> Dict:
    try:
        await delete_clear_herpetofauna(db, tower_number)
        return {"message": "Clear herpetofauna deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

"""
CRUD FOR CLEAR MAMMAL
"""

# Create clear mammal
@router.post(
    path="/api/clear_mammal/{tower_number}",
    response_model=ClearMammalResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["clear_mammal"],
    summary="Create clear mammal",
)
async def create_clear_mammal_api(
    tower_number: int,
    clear_mammal: ClearMammalBase,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"])),
) -> ClearMammalResponse | HTTPException:
    return await create_clear_mammal(db, clear_mammal, tower_number)

# Get all clear mammal
@router.get(
    path="/api/clear_mammal",
    response_model=List[ClearMammalResponse],
    tags=["clear_mammal"],
    summary="Get all clear mammal",
)
async def get_clear_mammal_api(
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"])),
) -> List[Clear_mammals]:
    clear_mammal: List[Clear_mammals]= await get_clear_mammal(db)
    return clear_mammal

# Get clear mammal by tower number
@router.get(
    path="/api/clear_mammal/{tower_number}",
    response_model=ClearMammalResponse,
    tags=["clear_mammal"],
    summary="Get clear mammal by id",
)
async def get_clear_mammal_by_tower_number_api(
    tower_number: int,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin", "user"])),
) -> Clear_mammals | None:
    return await get_clear_mammal_by_tower_number(db, tower_number)

# Update clear mammal
@router.put(
    path="/api/clear_mammal/{tower_number}",
    response_model=ClearMammalResponse,
    tags=["clear_mammal"],
    summary="Update clear mammal",
)
async def update_clear_mammal_api(
    tower_number: int,
    clear_mammal: ClearMammalBase,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"])),
) -> ClearMammalResponse:
    return await update_clear_mammal(db, clear_mammal,  tower_number )

# Delete clear mammal
@router.delete(
    path="/api/clear_mammal/{tower_number}",
    tags=["clear_mammal"],
    summary="Delete clear mammal",
)
async def delete_clear_mammal_api(
    tower_number: int,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"])),
) -> Dict:
    try:
        await delete_clear_mammal(db, tower_number)
        return {"message": "Clear mammal deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))




