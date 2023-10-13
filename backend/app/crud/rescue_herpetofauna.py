from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import HTTPException
from datetime import date

from app.schemas.rescue_herpetofauna import (
    # AgeGroup
    AgeGroupBase,
    AgeGroupCreate,

    # TransectHerpetofauna
    TransectHerpetofaunaBase,
    TransectHerpetofaunaCreate,

    # MarkHerpetofauna
    MarkHerpetofaunaBase,
    MarkHerpetofaunaCreate,
)

from app.models.rescue_herpetofauna import AgeGroup, MarkHerpetofauna, TransectHerpetofauna

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
CRUD FOR MARK HERPETOFAUNA
"""
#Get if mark herpetofauna exists by number
async def get_mark_herpetofauna_by_number(db: AsyncSession, number: str) -> MarkHerpetofauna | None:
    result = await db.execute(select(MarkHerpetofauna).where(MarkHerpetofauna.number == number))
    return result.scalars().first()

#Get mark herpetofauna by id
async def get_mark_herpetofauna_by_id(db: AsyncSession, id: int) -> MarkHerpetofauna | None:
    result = await db.execute(select(MarkHerpetofauna).where(MarkHerpetofauna.id == id))
    return result.scalars().first()

#Get all mark herpetofauna
async def get_all_mark_herpetofauna(db: AsyncSession) -> List[MarkHerpetofauna]:
    mark_herpetofauna_db = await db.execute(select(MarkHerpetofauna))
    return list(mark_herpetofauna_db.scalars().all())

#Create mark herpetofauna
async def create_mark_herpetofauna(db: AsyncSession, mark_herpetofauna: MarkHerpetofaunaBase) -> MarkHerpetofauna:
    mark_herpetofauna_db = MarkHerpetofauna(
        date=mark_herpetofauna.date,
        number=mark_herpetofauna.number,
        code=mark_herpetofauna.code,
        gender=mark_herpetofauna.gender,
        LHC=mark_herpetofauna.LHC,
        weight=mark_herpetofauna.weight,
        is_photo_mark = mark_herpetofauna.is_photo_mark,
        is_elastomer_mark = mark_herpetofauna.is_elastomer_mark,
        tower_id=mark_herpetofauna.tower_id,
        species_id=mark_herpetofauna.species_id,
        age_group_id=mark_herpetofauna.age_group_id,
    )
    db.add(mark_herpetofauna_db)
    await db.commit()
    await db.refresh(mark_herpetofauna_db)
    return mark_herpetofauna_db

#Update mark herpetofauna
async def update_mark_herpetofauna(db: AsyncSession, mark_herpetofauna_id: int , mark_herpetofauna_update: MarkHerpetofaunaBase) -> MarkHerpetofauna:
   result = await db.execute(select(MarkHerpetofauna).where(MarkHerpetofauna.id == mark_herpetofauna_id)) 
   mark_herpetofauna_db = result.scalars().first()
   if not mark_herpetofauna_db:
       raise HTTPException(status_code=404, detail="Mark herpetofauna not found")
   mark_herpetofauna_db.date = mark_herpetofauna_update.date
   mark_herpetofauna_db.number = mark_herpetofauna_update.number
   mark_herpetofauna_db.code = mark_herpetofauna_update.code
   mark_herpetofauna_db.gender = mark_herpetofauna_update.gender
   mark_herpetofauna_db.LHC = mark_herpetofauna_update.LHC
   mark_herpetofauna_db.weight = mark_herpetofauna_update.weight
   mark_herpetofauna_db.is_photo_mark = mark_herpetofauna_update.is_photo_mark
   mark_herpetofauna_db.is_elastomer_mark = mark_herpetofauna_update.is_elastomer_mark
   mark_herpetofauna_db.tower_id = mark_herpetofauna_update.tower_id
   mark_herpetofauna_db.species_id = mark_herpetofauna_update.species_id
   mark_herpetofauna_db.age_group_id = mark_herpetofauna_update.age_group_id
   await db.commit()
   await db.refresh(mark_herpetofauna_db)
   return mark_herpetofauna_db

#Delete mark herpetofauna
async def delete_mark_herpetofauna(db: AsyncSession, mark_herpetofauna_id: int) -> MarkHerpetofauna:
    result = await db.execute(select(MarkHerpetofauna).where(MarkHerpetofauna.id == mark_herpetofauna_id))
    mark_herpetofauna_db = result.scalars().first()
    if not mark_herpetofauna_db:
        raise HTTPException(status_code=404, detail="Mark herpetofauna not found")
    await db.execute(delete(MarkHerpetofauna).where(MarkHerpetofauna.id == mark_herpetofauna_id))
    await db.commit()
    return mark_herpetofauna_db






    



