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

    # RescueHerpetofauna
    RescueHerpetofaunaBase,
    RescueHerpetofaunaCreate,
)

from app.models.rescue_herpetofauna import (
    AgeGroup,
    MarkHerpetofauna,
    TransectHerpetofauna,
    RescueHerpetofauna
)

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
CRUD FOR TRANSECT HERPETOFAUNA
"""
#Get if transect herpetofauna exists by number
async def get_transect_herpetofauna_by_number(db: AsyncSession, number:int ) -> TransectHerpetofauna | None:
    result = await db.execute(select(TransectHerpetofauna).where(TransectHerpetofauna.number == number))
    return result.scalars().first()

#Get transect herpetofauna by id
async def get_transect_herpetofauna_by_id(db: AsyncSession, id: int) -> TransectHerpetofauna | None:
    result = await db.execute(select(TransectHerpetofauna).where(TransectHerpetofauna.id == id))
    return result.scalars().first()

#Get all transect herpetofauna
async def get_all_transect_herpetofauna(db: AsyncSession) -> List[TransectHerpetofauna]:
    transect_herpetofauna_db = await db.execute(select(TransectHerpetofauna))
    return list(transect_herpetofauna_db.scalars().all())

#Create transect herpetofauna
async def create_transect_herpetofauna(db: AsyncSession, transect_herpetofauna: TransectHerpetofaunaCreate) -> TransectHerpetofauna | HTTPException:
    #Check if transect herpetofauna exists
    transect_herpetofauna_db = TransectHerpetofauna(
        number=transect_herpetofauna.number,
        date_in = transect_herpetofauna.date_in,
        date_out = transect_herpetofauna.date_out,
        latitude_in = transect_herpetofauna.latitude_in,
        longitude_in = transect_herpetofauna.longitude_in,
        altitude_in = transect_herpetofauna.altitude_in,
        latitude_out = transect_herpetofauna.latitude_out,
        longitude_out = transect_herpetofauna.longitude_out,
        altitude_out = transect_herpetofauna.altitude_out,
        tower_id = transect_herpetofauna.tower_id,
        )
    db.add(transect_herpetofauna_db)
    await db.commit()
    await db.refresh(transect_herpetofauna_db)
    return transect_herpetofauna_db

#Update transect herpetofauna
async def update_transect_herpetofauna(db: AsyncSession, transect_herpetofauna_id: int , transect_herpetofauna_update: TransectHerpetofaunaBase) -> TransectHerpetofauna:
    result = await db.execute(select(TransectHerpetofauna).where(TransectHerpetofauna.id == transect_herpetofauna_id))
    transect_herpetofauna_db = result.scalars().first()
    if not transect_herpetofauna_db:
        raise HTTPException(status_code=404, detail="Transect herpetofauna not found")
    transect_herpetofauna_db.number = transect_herpetofauna_update.number
    transect_herpetofauna_db.date_in = transect_herpetofauna_update.date_in
    transect_herpetofauna_db.date_out = transect_herpetofauna_update.date_out
    transect_herpetofauna_db.latitude_in = transect_herpetofauna_update.latitude_in
    transect_herpetofauna_db.longitude_in = transect_herpetofauna_update.longitude_in
    transect_herpetofauna_db.altitude_in = transect_herpetofauna_update.altitude_in
    transect_herpetofauna_db.latitude_out = transect_herpetofauna_update.latitude_out
    transect_herpetofauna_db.longitude_out = transect_herpetofauna_update.longitude_out
    transect_herpetofauna_db.altitude_out = transect_herpetofauna_update.altitude_out
    transect_herpetofauna_db.tower_id = transect_herpetofauna_update.tower_id
    await db.commit()
    await db.refresh(transect_herpetofauna_db)
    return transect_herpetofauna_db

#Delete transect herpetofauna
async def delete_transect_herpetofauna(db: AsyncSession, transect_herpetofauna_id: int) -> TransectHerpetofauna:
    result = await db.execute(select(TransectHerpetofauna).where(TransectHerpetofauna.id == transect_herpetofauna_id))
    transect_herpetofauna_db = result.scalars().first()
    if not transect_herpetofauna_db:
        raise HTTPException(status_code=404, detail="Transect herpetofauna not found")
    await db.execute(delete(TransectHerpetofauna).where(TransectHerpetofauna.id == transect_herpetofauna_id))
    await db.commit()
    return transect_herpetofauna_db


"""
CRUD FOR MARK HERPETOFAUNA
"""
#Get if mark herpetofauna exists by number
async def get_mark_herpetofauna_by_number(db: AsyncSession, number:int ) -> MarkHerpetofauna | None:
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
        LHC=mark_herpetofauna.LHC,
        weight=mark_herpetofauna.weight,
        is_photo_mark = mark_herpetofauna.is_photo_mark,
        is_elastomer_mark = mark_herpetofauna.is_elastomer_mark,
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
   mark_herpetofauna_db.LHC = mark_herpetofauna_update.LHC
   mark_herpetofauna_db.weight = mark_herpetofauna_update.weight
   mark_herpetofauna_db.is_photo_mark = mark_herpetofauna_update.is_photo_mark
   mark_herpetofauna_db.is_elastomer_mark = mark_herpetofauna_update.is_elastomer_mark
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

"""
CRUD FOR RESCUE HERPETOFAUNA
"""

#Get if rescue herpetofauna exists by number
async def get_rescue_herpetofauna_by_number(db: AsyncSession, number:int ) -> RescueHerpetofauna | None:
    result = await db.execute(select(RescueHerpetofauna).where(RescueHerpetofauna.number == number))
    return result.scalars().first()

#Get rescue herpetofauna by id
async def get_rescue_herpetofauna_by_id(db: AsyncSession, id: int) -> RescueHerpetofauna | None:
    result = await db.execute(select(RescueHerpetofauna).where(RescueHerpetofauna.id == id))
    return result.scalars().first()

#Get all rescue herpetofauna
async def get_all_rescue_herpetofauna(db: AsyncSession) -> List[RescueHerpetofauna]:
    rescue_herpetofauna_db = await db.execute(select(RescueHerpetofauna))
    return list(rescue_herpetofauna_db.scalars().all())

#Create rescue herpetofauna
async def create_rescue_herpetofauna(db: AsyncSession, rescue_herpetofauna: RescueHerpetofaunaCreate) -> RescueHerpetofauna:
    rescue_herpetofauna_db = RescueHerpetofauna(
        number=rescue_herpetofauna.number,
        gender=rescue_herpetofauna.gender,
        specie_id=rescue_herpetofauna.specie_id,
        mark_herpetofauna_id=rescue_herpetofauna.mark_herpetofauna_id,
        transect_herpetofauna_id=rescue_herpetofauna.transect_herpetofauna_id,
        age_group_id=rescue_herpetofauna.age_group_id,
    )
    db.add(rescue_herpetofauna_db)
    await db.commit()
    await db.refresh(rescue_herpetofauna_db)
    return rescue_herpetofauna_db

#Update rescue herpetofauna
async def update_rescue_herpetofauna(db: AsyncSession, rescue_herpetofauna_id: int , rescue_herpetofauna_update: RescueHerpetofaunaBase) -> RescueHerpetofauna:
    result = await db.execute(select(RescueHerpetofauna).where(RescueHerpetofauna.id == rescue_herpetofauna_id))
    rescue_herpetofauna_db = result.scalars().first()
    if not rescue_herpetofauna_db:
        raise HTTPException(status_code=404, detail="Rescue herpetofauna not found")
    rescue_herpetofauna_db.number = rescue_herpetofauna_update.number
    rescue_herpetofauna_db.gender = rescue_herpetofauna_update.gender
    rescue_herpetofauna_db.specie_id = rescue_herpetofauna_update.specie_id
    rescue_herpetofauna_db.mark_herpetofauna_id = rescue_herpetofauna_update.mark_herpetofauna_id
    rescue_herpetofauna_db.transect_herpetofauna_id = rescue_herpetofauna_update.transect_herpetofauna_id
    rescue_herpetofauna_db.age_group_id = rescue_herpetofauna_update.age_group_id
    await db.commit()
    await db.refresh(rescue_herpetofauna_db)
    return rescue_herpetofauna_db

#Delete rescue herpetofauna
async def delete_rescue_herpetofauna(db: AsyncSession, rescue_herpetofauna_id: int) -> RescueHerpetofauna:
    result = await db.execute(select(RescueHerpetofauna).where(RescueHerpetofauna.id == rescue_herpetofauna_id))
    rescue_herpetofauna_db = result.scalars().first()
    if not rescue_herpetofauna_db:
        raise HTTPException(status_code=404, detail="Rescue herpetofauna not found")
    await db.execute(delete(RescueHerpetofauna).where(RescueHerpetofauna.id == rescue_herpetofauna_id))
    await db.commit()
    return rescue_herpetofauna_db



