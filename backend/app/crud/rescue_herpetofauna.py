from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import HTTPException
from datetime import date

from app.schemas.rescue_herpetofauna import (
    # AgeGroup
    AgeGroupBase,
    AgeGroupCreate,
    AgeGroupResponse,

    # RescueHerpetofauna
    RescueHerpetofaunaBase,
    RescueHerpetofaunaCreate,
    RescueHerpetofaunaResponse
)

from app.models.rescue_herpetofauna import AgeGroup, RescueHerpetofauna

# Purpose: CRUD operations for RescueHerpetofauna
"""
CRUD FOR AGE GROUP
"""

#Get if age group name exists
async def get_age_group_name(db: AsyncSession, name: str) -> AgeGroup | None:
    result = await db.execute(select(AgeGroup).where(AgeGroup.name == name))
    return result.scalars().first()

#Get age group by id
async def get_age_group_by_id(db: AsyncSession, id: int) -> AgeGroup | None:
    result = await db.execute(select(AgeGroup).where(AgeGroup.id == id))
    return result.scalars().first()

#Get all age groups
async def get_all_age_groups(db: AsyncSession) -> List[AgeGroup]:
    age_groups_db = await db.execute(select(AgeGroup))
    return list(age_groups_db.scalars().all())

#Create age group
async def create_age_group(db: AsyncSession, age_group: AgeGroupCreate) -> AgeGroup:
    age_group_db = AgeGroup(name=age_group.name)
    db.add(age_group_db)
    await db.commit()
    await db.refresh(age_group_db)
    return age_group_db

#Update age group
async def update_age_group(db: AsyncSession, age_group_id: int , age_group_update: AgeGroupBase) -> AgeGroup:
    result = await db.execute(select(AgeGroup).where(AgeGroup.id == age_group_id))
    age_group_db = result.scalars().first()
    if not age_group_db:
        raise HTTPException(status_code=404, detail="Age group not found")
    age_group_db.name = age_group_update.name
    await db.commit()
    await db.refresh(age_group_db)
    return age_group_db

#Delete age group
async def delete_age_group(db: AsyncSession, age_group_id: int) -> AgeGroup:
    result = await db.execute(select(AgeGroup).where(AgeGroup.id == age_group_id))
    age_group_db = result.scalars().first()
    if not age_group_db:
        raise HTTPException(status_code=404, detail="Age group not found")
    await db.execute(delete(AgeGroup).where(AgeGroup.id == age_group_id))
    await db.commit()
    return age_group_db

"""
CRUD FOR RESCUE HERPETOFAUNA
"""
#Get rescue herpetofauna by id
async def get_rescue_herpetofauna_by_id(db: AsyncSession, id: int) -> RescueHerpetofauna | None:
    result = await db.execute(select(RescueHerpetofauna).where(RescueHerpetofauna.id == id))
    return result.scalars().first()

#Get all rescue herpetofauna
async def get_all_rescue_herpetofauna(db: AsyncSession) -> List[RescueHerpetofauna]:
    rescue_herpetofauna_db = await db.execute(select(RescueHerpetofauna))
    return list(rescue_herpetofauna_db.scalars().all())


