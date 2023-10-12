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
)

from app.models.rescue_herpetofauna import AgeGroup

from app.crud.rescue_herpetofauna import (
    # AgeGroup
    get_age_group_name,
    get_age_group_by_id,
    get_all_age_groups,
    create_age_group,
    update_age_group,
    delete_age_group,


    # MarkHerpetofauna
    get_mark_herpetofauna_by_number,
    get_mark_herpetofauna_by_id,
    get_all_mark_herpetofauna,
    create_mark_herpetofauna,
    update_mark_herpetofauna,
    delete_mark_herpetofauna,
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


