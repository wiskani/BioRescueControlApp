from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Union, Dict

from app.schemas.rescue_herpetofauna import (
    # AgeGroup
    AgeGroupBase,
    AgeGroupCreate,
    AgeGroupResponse,

    # TransectHerpetofauna
    TransectHerpetofaunaBase,
    TransectHerpetofaunaCreate,
    TransectHerpetofaunaResponse,

    # MarkHerpetofauna
    MarkHerpetofaunaBase,
    MarkHerpetofaunaCreate,
    MarkHerpetofaunaResponse,

    # RescueHerpetofauna
    RescueHerpetofaunaBase,
    RescueHerpetofaunaCreate,
    RescueHerpetofaunaResponse,
)

from app.models.rescue_herpetofauna import (
    AgeGroup,
    MarkHerpetofauna,
    TransectHerpetofauna,
    RescueHerpetofauna,
)

from app.crud.rescue_herpetofauna import (
    # AgeGroup
    get_age_group_name,
    get_age_group_by_id,
    get_all_age_groups,
    create_age_group,
    update_age_group,
    delete_age_group,

    # TransectHerpetofauna
    get_transect_herpetofauna_by_number,
    get_transect_herpetofauna_by_id,
    get_all_transect_herpetofauna,
    create_transect_herpetofauna,
    update_transect_herpetofauna,
    delete_transect_herpetofauna,

    # MarkHerpetofauna
    get_mark_herpetofauna_by_number,
    get_mark_herpetofauna_by_id,
    get_all_mark_herpetofauna,
    create_mark_herpetofauna,
    update_mark_herpetofauna,
    delete_mark_herpetofauna,

    # RescueHerpetofauna
    get_rescue_herpetofauna_by_number,
    get_rescue_herpetofauna_by_id,
    get_all_rescue_herpetofauna,
    create_rescue_herpetofauna,
    update_rescue_herpetofauna,
    delete_rescue_herpetofauna,
)

from app.api.deps import PermissonsChecker, get_db

router: APIRouter = APIRouter()

#Create age group
@router.post(
    path="/api/age_group",
    response_model=AgeGroupResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Age Group"],
    summary="Create age group",
)
async def create_age_group_api(
    new_age_group: AgeGroupCreate,
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> AgeGroup|HTTPException:
    age_group_db = await get_age_group_name(db, new_age_group.name)
    if age_group_db:
        raise HTTPException(status_code=400, detail="Age group name already exists")
    return await create_age_group(db, new_age_group)

#Get all age groups
@router.get(
    path="/api/age_group",
    response_model=List[AgeGroupResponse],
    status_code=status.HTTP_200_OK,
    tags=["Age Group"],
    summary="Get all age groups",
)
async def get_all_age_groups_api(
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> List[AgeGroup]:
    return await get_all_age_groups(db)

#Get age group by id
@router.get(
    path="/api/age_group/{age_group_id}",
    response_model=AgeGroupResponse,
    status_code=status.HTTP_200_OK,
    tags=["Age Group"],
    summary="Get age group by id",
)
async def get_age_group_by_id_api(
    age_group_id: int,
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> AgeGroup|HTTPException:
    age_group_db = await get_age_group_by_id(db, age_group_id)
    if not age_group_db:
        raise HTTPException(status_code=404, detail="Age group not found")
    return age_group_db

#Update age group
@router.put(
    path="/api/age_group/{age_group_id}",
    response_model=AgeGroupResponse,
    status_code=status.HTTP_200_OK,
    tags=["Age Group"],
    summary="Update age group",
)
async def update_age_group_api(
    age_group_id: int,
    age_group_update: AgeGroupBase,
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> AgeGroup|HTTPException:
    return await update_age_group(db, age_group_id, age_group_update)

#Delete age group
@router.delete(
    path="/api/age_group/{age_group_id}",
    response_model=None,
    status_code=status.HTTP_200_OK,
    tags=["Age Group"],
    summary="Delete age group",
)
async def delete_age_group_api(
    age_group_id: int,
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> Dict|HTTPException:
    db_age_group = await get_age_group_by_id(db, age_group_id)
    if not db_age_group:
        raise HTTPException(status_code=404, detail="Age group not found")
    await delete_age_group(db, age_group_id)
    return {"detail": "Age group deleted successfully"}

#Create transect herpetofauna
@router.post(
    path="/api/transect_herpetofauna",
    response_model=TransectHerpetofaunaResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Transect Herpetofauna"],
    summary="Create transect herpetofauna",
)
async def create_transect_herpetofauna_api(
    new_transect_herpetofauna: TransectHerpetofaunaCreate,
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> TransectHerpetofauna|HTTPException:
    transect_herpetofauna_db = await get_transect_herpetofauna_by_number(db, new_transect_herpetofauna.number)
    if transect_herpetofauna_db:
        raise HTTPException(status_code=400, detail="Transect herpetofauna number already exists")
    return await create_transect_herpetofauna(db, new_transect_herpetofauna)

#Get all transect herpetofauna
@router.get(
    path="/api/transect_herpetofauna",
    response_model=List[TransectHerpetofaunaResponse],
    status_code=status.HTTP_200_OK,
    tags=["Transect Herpetofauna"],
    summary="Get all transect herpetofauna",
)
async def get_all_transect_herpetofauna_api(
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> List[TransectHerpetofauna]:
    return await get_all_transect_herpetofauna(db)

#Get transect herpetofauna by id
@router.get(
    path="/api/transect_herpetofauna/{transect_herpetofauna_id}",
    response_model=TransectHerpetofaunaResponse,
    status_code=status.HTTP_200_OK,
    tags=["Transect Herpetofauna"],
    summary="Get transect herpetofauna by id",
)
async def get_transect_herpetofauna_by_id_api(
    transect_herpetofauna_id: int,
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> TransectHerpetofauna|HTTPException:
    transect_herpetofauna_db = await get_transect_herpetofauna_by_id(db, transect_herpetofauna_id)
    if not transect_herpetofauna_db:
        raise HTTPException(status_code=404, detail="Transect herpetofauna not found")
    return transect_herpetofauna_db

#Update transect herpetofauna
@router.put(
    path="/api/transect_herpetofauna/{transect_herpetofauna_id}",
    response_model=TransectHerpetofaunaResponse,
    status_code=status.HTTP_200_OK,
    tags=["Transect Herpetofauna"],
    summary="Update transect herpetofauna",
)
async def update_transect_herpetofauna_api(
    transect_herpetofauna_id: int,
    transect_herpetofauna_update: TransectHerpetofaunaBase,
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> TransectHerpetofauna|HTTPException:
    return await update_transect_herpetofauna(db, transect_herpetofauna_id, transect_herpetofauna_update)

#Delete transect herpetofauna
@router.delete(
    path="/api/transect_herpetofauna/{transect_herpetofauna_id}",
    response_model=None,
    status_code=status.HTTP_200_OK,
    tags=["Transect Herpetofauna"],
    summary="Delete transect herpetofauna",
)
async def delete_transect_herpetofauna_api(
    transect_herpetofauna_id: int,
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> Dict|HTTPException:
    db_transect_herpetofauna = await get_transect_herpetofauna_by_id(db, transect_herpetofauna_id)
    if not db_transect_herpetofauna:
        raise HTTPException(status_code=404, detail="Transect herpetofauna not found")
    await delete_transect_herpetofauna(db, transect_herpetofauna_id)
    return {"detail": "Transect herpetofauna deleted successfully"}


#Create mark herpetofauna
@router.post(
    path="/api/mark_herpetofauna",
    response_model=MarkHerpetofaunaResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Mark Herpetofauna"],
    summary="Create mark herpetofauna",
)
async def create_mark_herpetofauna_api(
    new_mark_herpetofauna: MarkHerpetofaunaCreate,
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> MarkHerpetofauna|HTTPException:
    mark_herpetofauna_db = await get_mark_herpetofauna_by_number(db, new_mark_herpetofauna.number)
    if mark_herpetofauna_db:
        raise HTTPException(status_code=400, detail="Mark herpetofauna number already exists")
    return await create_mark_herpetofauna(db, new_mark_herpetofauna)

#Get all mark herpetofauna
@router.get(
    path="/api/mark_herpetofauna",
    response_model=List[MarkHerpetofaunaResponse],
    status_code=status.HTTP_200_OK,
    tags=["Mark Herpetofauna"],
    summary="Get all mark herpetofauna",
)
async def get_all_mark_herpetofauna_api(
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> List[MarkHerpetofauna]:
    return await get_all_mark_herpetofauna(db)

#Get mark herpetofauna by id
@router.get(
    path="/api/mark_herpetofauna/{mark_herpetofauna_id}",
    response_model=MarkHerpetofaunaResponse,
    status_code=status.HTTP_200_OK,
    tags=["Mark Herpetofauna"],
    summary="Get mark herpetofauna by id",
)
async def get_mark_herpetofauna_by_id_api(
    mark_herpetofauna_id: int,
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> MarkHerpetofauna|HTTPException:
    mark_herpetofauna_db = await get_mark_herpetofauna_by_id(db, mark_herpetofauna_id)
    if not mark_herpetofauna_db:
        raise HTTPException(status_code=404, detail="Mark herpetofauna not found")
    return mark_herpetofauna_db

#Update mark herpetofauna
@router.put(
    path="/api/mark_herpetofauna/{mark_herpetofauna_id}",
    response_model=MarkHerpetofaunaResponse,
    status_code=status.HTTP_200_OK,
    tags=["Mark Herpetofauna"],
    summary="Update mark herpetofauna",
)
async def update_mark_herpetofauna_api(
    mark_herpetofauna_id: int,
    mark_herpetofauna_update: MarkHerpetofaunaBase,
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> MarkHerpetofauna|HTTPException:
    return await update_mark_herpetofauna(db, mark_herpetofauna_id, mark_herpetofauna_update)

#Delete mark herpetofauna
@router.delete(
    path="/api/mark_herpetofauna/{mark_herpetofauna_id}",
    response_model=None,
    status_code=status.HTTP_200_OK,
    tags=["Mark Herpetofauna"],
    summary="Delete mark herpetofauna",
)
async def delete_mark_herpetofauna_api(
    mark_herpetofauna_id: int,
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> Dict|HTTPException:
    db_mark_herpetofauna = await get_mark_herpetofauna_by_id(db, mark_herpetofauna_id)
    if not db_mark_herpetofauna:
        raise HTTPException(status_code=404, detail="Mark herpetofauna not found")
    await delete_mark_herpetofauna(db, mark_herpetofauna_id)
    return {"detail": "Mark herpetofauna deleted successfully"}

#Create rescue herpetofauna
@router.post(
    path="/api/rescue_herpetofauna",
    response_model=RescueHerpetofaunaResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Rescue Herpetofauna"],
    summary="Create rescue herpetofauna",
)
async def create_rescue_herpetofauna_api(
    new_rescue_herpetofauna: RescueHerpetofaunaCreate,
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> RescueHerpetofauna|HTTPException:
    rescue_herpetofauna_db = await get_rescue_herpetofauna_by_number(db, new_rescue_herpetofauna.number)
    if rescue_herpetofauna_db:
        raise HTTPException(status_code=400, detail="Rescue herpetofauna number already exists")
    return await create_rescue_herpetofauna(db, new_rescue_herpetofauna)

#Get all rescue herpetofauna
@router.get(
    path="/api/rescue_herpetofauna",
    response_model=List[RescueHerpetofaunaResponse],
    status_code=status.HTTP_200_OK,
    tags=["Rescue Herpetofauna"],
    summary="Get all rescue herpetofauna",
)
async def get_all_rescue_herpetofauna_api(
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> List[RescueHerpetofauna]:
    return await get_all_rescue_herpetofauna(db)

#Get rescue herpetofauna by id
@router.get(
    path="/api/rescue_herpetofauna/{rescue_herpetofauna_id}",
    response_model=RescueHerpetofaunaResponse,
    status_code=status.HTTP_200_OK,
    tags=["Rescue Herpetofauna"],
    summary="Get rescue herpetofauna by id",
)
async def get_rescue_herpetofauna_by_id_api(
    rescue_herpetofauna_id: int,
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> RescueHerpetofauna|HTTPException:
    rescue_herpetofauna_db = await get_rescue_herpetofauna_by_id(db, rescue_herpetofauna_id)
    if not rescue_herpetofauna_db:
        raise HTTPException(status_code=404, detail="Rescue herpetofauna not found")
    return rescue_herpetofauna_db

#Update rescue herpetofauna
@router.put(
    path="/api/rescue_herpetofauna/{rescue_herpetofauna_id}",
    response_model=RescueHerpetofaunaResponse,
    status_code=status.HTTP_200_OK,
    tags=["Rescue Herpetofauna"],
    summary="Update rescue herpetofauna",
)
async def update_rescue_herpetofauna_api(
    rescue_herpetofauna_id: int,
    rescue_herpetofauna_update: RescueHerpetofaunaBase,
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> RescueHerpetofauna|HTTPException:
    return await update_rescue_herpetofauna(db, rescue_herpetofauna_id, rescue_herpetofauna_update)

#Delete rescue herpetofauna
@router.delete(
    path="/api/rescue_herpetofauna/{rescue_herpetofauna_id}",
    response_model=None,
    status_code=status.HTTP_200_OK,
    tags=["Rescue Herpetofauna"],
    summary="Delete rescue herpetofauna",
)
async def delete_rescue_herpetofauna_api(
    rescue_herpetofauna_id: int,
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> Dict|HTTPException:
    db_rescue_herpetofauna = await get_rescue_herpetofauna_by_id(db, rescue_herpetofauna_id)
    if not db_rescue_herpetofauna:
        raise HTTPException(status_code=404, detail="Rescue herpetofauna not found")
    await delete_rescue_herpetofauna(db, rescue_herpetofauna_id)
    return {"detail": "Rescue herpetofauna deleted successfully"}

