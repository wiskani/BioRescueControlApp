from app.crud.species import get_specie_by_id
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import HTTPException

from app.schemas.rescue_herpetofauna import (
    # AgeGroup
    AgeGroupBase,
    AgeGroupCreate,

    # TransectHerpetofauna
    TransectHerpetofaunaBase,
    TransectHerpetofaunaCreate,

    # MarkHerpetofauna
    MarkHerpetofaunaBase,

    # RescueHerpetofauna
    RescueHerpetofaunaBase,
    RescueHerpetofaunaCreate,

    # TransectHerpetofaunaTranslocation
    TransectHerpetofaunaTranslocationBase,
    TransectHerpetofaunaTranslocationCreate,

    # PointTransectHerpetofauna
    PointHerpetofaunaTranslocationBase,
    PointHerpetofaunaTranslocationCreate,


    # TranslocationHerpetofauna
    TranslocationHerpetofaunaBase,
    TranslocationHerpetofaunaCreate,

    # Transect_herpetofauna_with_species
    TransectHerpetoWithSpecies,
    TransectHerpetoTransWithSpecies,
    PointHerpetoTransloWithSpecies,

    # Rescue with species
    RescueHerpetoWithSpecies,
    PointTranslocationHerpetoWithMark,
    TransectTranslocationHerpetoWithMark,
)

from app.models.rescue_herpetofauna import (
    AgeGroup,
    MarkHerpetofauna,
    TransectHerpetofauna,
    RescueHerpetofauna,
    TransectHerpetofaunaTranslocation,
    PointHerpetofaunaTranslocation,
    TranslocationHerpetofauna,
)

# Purpose: CRUD operations for RescueHerpetofauna
"""
CRUD FOR AGE GROUP
"""


# Get if age group name exists
async def get_age_group_name(db: AsyncSession, name: str) -> AgeGroup | None:
    """Get if age group name exists"""
    result = await db.execute(select(AgeGroup).where(AgeGroup.name == name))
    return result.scalars().first()


# Get age group by id
async def get_age_group_by_id(db: AsyncSession, id: int) -> AgeGroup | None:
    """Get age group by id"""
    result = await db.execute(select(AgeGroup).where(AgeGroup.id == id))
    return result.scalars().first()


# Get all age groups
async def get_all_age_groups(db: AsyncSession) -> List[AgeGroup]:
    """Get all age groups"""
    age_groups_db = await db.execute(select(AgeGroup))
    return list(age_groups_db.scalars().all())


# Create age group
async def create_age_group(
        db: AsyncSession,
        age_group: AgeGroupCreate
        ) -> AgeGroup:
    """Create age group"""
    age_group_db = AgeGroup(name=age_group.name)
    db.add(age_group_db)
    await db.commit()
    await db.refresh(age_group_db)
    return age_group_db


# Update age group
async def update_age_group(
        db: AsyncSession,
        age_group_id: int,
        age_group_update: AgeGroupBase
        ) -> AgeGroup:
    """Update age group"""
    result = await db.execute(
            select(AgeGroup).where(AgeGroup.id == age_group_id)
            )
    age_group_db = result.scalars().first()
    if not age_group_db:
        raise HTTPException(status_code=404, detail="Age group not found")
    age_group_db.name = age_group_update.name
    await db.commit()
    await db.refresh(age_group_db)
    return age_group_db


# Delete age group
async def delete_age_group(
        db: AsyncSession,
        age_group_id: int
        ) -> AgeGroup:
    """Delete age group"""
    result = await db.execute(
            select(AgeGroup).
            where(AgeGroup.id == age_group_id)
            )
    age_group_db = result.scalars().first()
    if not age_group_db:
        raise HTTPException(status_code=404, detail="Age group not found")
    await db.execute(delete(AgeGroup).where(AgeGroup.id == age_group_id))
    await db.commit()
    return age_group_db

"""
CRUD FOR TRANSECT HERPETOFAUNA
"""


# Get if transect herpetofauna exists by number
async def get_transect_herpetofauna_by_number(
        db: AsyncSession,
        number: str
        ) -> TransectHerpetofauna | None:
    result = await db.execute(
            select(TransectHerpetofauna)
            .where(TransectHerpetofauna.number == number)
            )
    return result.scalars().first()


# Get transect herpetofauna by id
async def get_transect_herpetofauna_by_id(
        db: AsyncSession,
        id: int
        ) -> TransectHerpetofauna | None:
    result = await db.execute(
            select(TransectHerpetofauna)
            .where(TransectHerpetofauna.id == id)
            )
    return result.scalars().first()


# Get all transect herpetofauna
async def get_all_transect_herpetofauna(
        db: AsyncSession
        ) -> List[TransectHerpetofauna]:
    transect_herpetofauna_db = await db.execute(select(TransectHerpetofauna))
    return list(transect_herpetofauna_db.scalars().all())


# Create transect herpetofauna
async def create_transect_herpetofauna(
        db: AsyncSession,
        transect_herpetofauna: TransectHerpetofaunaCreate
        ) -> TransectHerpetofauna | HTTPException:
    """Create transect herpetofauna"""
    # Check if transect herpetofauna exists
    transect_herpetofauna_db = TransectHerpetofauna(
        number=transect_herpetofauna.number,
        date_in=transect_herpetofauna.date_in,
        date_out=transect_herpetofauna.date_out,
        latitude_in=transect_herpetofauna.latitude_in,
        longitude_in=transect_herpetofauna.longitude_in,
        altitude_in=transect_herpetofauna.altitude_in,
        latitude_out=transect_herpetofauna.latitude_out,
        longitude_out=transect_herpetofauna.longitude_out,
        altitude_out=transect_herpetofauna.altitude_out,
        tower_id=transect_herpetofauna.tower_id,
        )
    db.add(transect_herpetofauna_db)
    await db.commit()
    await db.refresh(transect_herpetofauna_db)
    return transect_herpetofauna_db


# Update transect herpetofauna
async def update_transect_herpetofauna(
        db: AsyncSession,
        transect_herpetofauna_id: int,
        transect_herpetofauna_update: TransectHerpetofaunaBase
        ) -> TransectHerpetofauna:
    result = await db.execute(
            select(TransectHerpetofauna)
            .where(TransectHerpetofauna.id == transect_herpetofauna_id)
            )
    transect_herpetofauna_db = result.scalars().first()
    if not transect_herpetofauna_db:
        raise HTTPException(
                status_code=404,
                detail="Transect herpetofauna not found"
                )
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


# Delete transect herpetofauna
async def delete_transect_herpetofauna(
        db: AsyncSession,
        transect_herpetofauna_id: int
        ) -> TransectHerpetofauna:
    result = await db.execute(
            select(TransectHerpetofauna)
            .where(TransectHerpetofauna.id == transect_herpetofauna_id)
            )
    transect_herpetofauna_db = result.scalars().first()
    if not transect_herpetofauna_db:
        raise HTTPException(
                status_code=404,
                detail="Transect herpetofauna not found"
                )
    await db.execute(
            delete(TransectHerpetofauna)
            .where(TransectHerpetofauna.id == transect_herpetofauna_id)
            )
    await db.commit()
    return transect_herpetofauna_db


"""
CRUD FOR MARK HERPETOFAUNA
"""


# Get if mark herpetofauna exists by number
async def get_mark_herpetofauna_by_number(
        db: AsyncSession,
        number: int
        ) -> MarkHerpetofauna | None:
    result = await db.execute(
            select(MarkHerpetofauna)
            .where(MarkHerpetofauna.number == number)
            )
    return result.scalars().first()


# Get mark herpetofauna by id
async def get_mark_herpetofauna_by_id(
        db: AsyncSession,
        id: int
        ) -> MarkHerpetofauna | None:
    result = await db.execute(
            select(MarkHerpetofauna)
            .where(MarkHerpetofauna.id == id)
            )
    return result.scalars().first()


# Get all mark herpetofauna
async def get_all_mark_herpetofauna(
        db: AsyncSession
        ) -> List[MarkHerpetofauna]:
    mark_herpetofauna_db = await db.execute(select(MarkHerpetofauna))
    return list(mark_herpetofauna_db.scalars().all())


# Create mark herpetofauna
async def create_mark_herpetofauna(
        db: AsyncSession,
        mark_herpetofauna: MarkHerpetofaunaBase
        ) -> MarkHerpetofauna:
    mark_herpetofauna_db = MarkHerpetofauna(
        date=mark_herpetofauna.date,
        number=mark_herpetofauna.number,
        code=mark_herpetofauna.code,
        LHC=mark_herpetofauna.LHC,
        weight=mark_herpetofauna.weight,
        is_photo_mark=mark_herpetofauna.is_photo_mark,
        is_elastomer_mark=mark_herpetofauna.is_elastomer_mark,
        rescue_herpetofauna_id=mark_herpetofauna.rescue_herpetofauna_id,
    )
    db.add(mark_herpetofauna_db)
    await db.commit()
    await db.refresh(mark_herpetofauna_db)
    return mark_herpetofauna_db


# Update mark herpetofauna
async def update_mark_herpetofauna(
        db: AsyncSession,
        mark_herpetofauna_id: int,
        mark_herpetofauna_update: MarkHerpetofaunaBase
        ) -> MarkHerpetofauna:
    result = await db.execute(
            select(MarkHerpetofauna)
            .where(
                MarkHerpetofauna.id == mark_herpetofauna_id
                ))
    mark_herpetofauna_db = result.scalars().first()
    if not mark_herpetofauna_db:
        raise HTTPException(
                status_code=404,
                detail="Mark herpetofauna not found"
                )
    mark_herpetofauna_db.date = mark_herpetofauna_update.date
    mark_herpetofauna_db.number = mark_herpetofauna_update.number
    mark_herpetofauna_db.code = mark_herpetofauna_update.code
    mark_herpetofauna_db.LHC = mark_herpetofauna_update.LHC
    mark_herpetofauna_db.weight = mark_herpetofauna_update.weight
    mark_herpetofauna_db.is_photo_mark = mark_herpetofauna_update.is_photo_mark
    mark_herpetofauna_db.is_elastomer_mark = mark_herpetofauna_update.is_elastomer_mark
    mark_herpetofauna_db.rescue_herpetofauna_id = mark_herpetofauna_update.rescue_herpetofauna_id
    await db.commit()
    await db.refresh(mark_herpetofauna_db)
    return mark_herpetofauna_db


# Delete mark herpetofauna
async def delete_mark_herpetofauna(
        db: AsyncSession,
        mark_herpetofauna_id: int
        ) -> MarkHerpetofauna:
    result = await db.execute(
            select(MarkHerpetofauna)
            .where(
                MarkHerpetofauna.id == mark_herpetofauna_id
                )
            )
    mark_herpetofauna_db = result.scalars().first()
    if not mark_herpetofauna_db:
        raise HTTPException(
                status_code=404,
                detail="Mark herpetofauna not found"
                )
    await db.execute(
            delete(MarkHerpetofauna)
            .where(
                MarkHerpetofauna.id == mark_herpetofauna_id
                ))
    await db.commit()
    return mark_herpetofauna_db

"""
CRUD FOR RESCUE HERPETOFAUNA
"""


# Get if rescue herpetofauna exists by number
async def get_rescue_herpetofauna_by_number(
        db: AsyncSession,
        number: str
        ) -> RescueHerpetofauna | None:
    result = await db.execute(
            select(RescueHerpetofauna)
            .where(
                RescueHerpetofauna.number == number
                   )
            )
    return result.scalars().first()


# Get rescue herpetofauna by id
async def get_rescue_herpetofauna_by_id(
        db: AsyncSession,
        id: int
        ) -> RescueHerpetofauna | None:
    result = await db.execute(
            select(RescueHerpetofauna).where(RescueHerpetofauna.id == id)
            )
    return result.scalars().first()


# Get all rescue herpetofauna
async def get_all_rescue_herpetofauna(
        db: AsyncSession
        ) -> List[RescueHerpetofauna]:
    rescue_herpetofauna_db = await db.execute(select(RescueHerpetofauna))
    return list(rescue_herpetofauna_db.scalars().all())


# Create rescue herpetofauna
async def create_rescue_herpetofauna(
        db: AsyncSession,
        rescue_herpetofauna: RescueHerpetofaunaCreate
        ) -> RescueHerpetofauna:
    rescue_herpetofauna_db = RescueHerpetofauna(
        number=rescue_herpetofauna.number,
        gender=rescue_herpetofauna.gender,
        specie_id=rescue_herpetofauna.specie_id,
        transect_herpetofauna_id=rescue_herpetofauna.transect_herpetofauna_id,
        age_group_id=rescue_herpetofauna.age_group_id,
    )
    db.add(rescue_herpetofauna_db)
    await db.commit()
    await db.refresh(rescue_herpetofauna_db)
    return rescue_herpetofauna_db


# Update rescue herpetofauna
async def update_rescue_herpetofauna(
        db: AsyncSession,
        rescue_herpetofauna_id: int,
        rescue_herpetofauna_update: RescueHerpetofaunaBase
        ) -> RescueHerpetofauna:
    result = await db.execute(
            select(RescueHerpetofauna)
            .where(RescueHerpetofauna.id == rescue_herpetofauna_id
                   )
            )
    rescue_herpetofauna_db = result.scalars().first()
    if not rescue_herpetofauna_db:
        raise HTTPException(
                status_code=404,
                detail="Rescue herpetofauna not found"
                )
    rescue_herpetofauna_db.number = rescue_herpetofauna_update.number
    rescue_herpetofauna_db.gender = rescue_herpetofauna_update.gender
    rescue_herpetofauna_db.specie_id = rescue_herpetofauna_update.specie_id
    rescue_herpetofauna_db.transect_herpetofauna_id = rescue_herpetofauna_update.transect_herpetofauna_id
    rescue_herpetofauna_db.age_group_id = rescue_herpetofauna_update.age_group_id
    await db.commit()
    await db.refresh(rescue_herpetofauna_db)
    return rescue_herpetofauna_db


# Delete rescue herpetofauna
async def delete_rescue_herpetofauna(
        db: AsyncSession,
        rescue_herpetofauna_id: int
        ) -> RescueHerpetofauna:
    result = await db.execute(
            select(RescueHerpetofauna)
            .where(RescueHerpetofauna.id == rescue_herpetofauna_id
                   )
            )
    rescue_herpetofauna_db = result.scalars().first()
    if not rescue_herpetofauna_db:
        raise HTTPException(status_code=404, detail="Rescue herpetofauna not found")
    await db.execute(delete(RescueHerpetofauna).where(RescueHerpetofauna.id == rescue_herpetofauna_id))
    await db.commit()
    return rescue_herpetofauna_db

"""
CRUD FOR TRANSECT HERPETOFAUNA TRANSLOCATION
"""


# Get if transect herpetofauna translocation exists by cod
async def get_transect_herpetofauna_translocation_by_cod(
        db: AsyncSession,
        cod: str
        ) -> TransectHerpetofaunaTranslocation | None:
    result = await db.execute(
            select(TransectHerpetofaunaTranslocation)
            .where(TransectHerpetofaunaTranslocation.cod == cod
                   )
            )
    return result.scalars().first()


# Get transect herpetofauna translocation by id
async def get_transect_herpetofauna_translocation_by_id(
        db: AsyncSession,
        id: int
        ) -> TransectHerpetofaunaTranslocation | None:
    result = await db.execute(
            select(TransectHerpetofaunaTranslocation)
            .where(TransectHerpetofaunaTranslocation.id == id)
            )
    return result.scalars().first()


# Get all transect herpetofauna translocation
async def get_all_transect_herpetofauna_translocation(
        db: AsyncSession
        ) -> List[TransectHerpetofaunaTranslocation]:
    transect_herpetofauna_translocation_db = await db.execute(
            select(TransectHerpetofaunaTranslocation)
            )
    return list(transect_herpetofauna_translocation_db.scalars().all())

#Create transect herpetofauna translocation
async def create_transect_herpetofauna_translocation(
        db: AsyncSession,
        transect_herpetofauna_translocation: TransectHerpetofaunaTranslocationCreate
        ) -> TransectHerpetofaunaTranslocation:
    transect_herpetofauna_translocation_db = TransectHerpetofaunaTranslocation(
        cod = transect_herpetofauna_translocation.cod,
        date = transect_herpetofauna_translocation.date,
        latitude_in = transect_herpetofauna_translocation.latitude_in,
        longitude_in = transect_herpetofauna_translocation.longitude_in,
        altitude_in = transect_herpetofauna_translocation.altitude_in,
        latitude_out = transect_herpetofauna_translocation.latitude_out,
        longitude_out = transect_herpetofauna_translocation.longitude_out,
        altitude_out = transect_herpetofauna_translocation.altitude_out,
    )
    db.add(transect_herpetofauna_translocation_db)
    await db.commit()
    await db.refresh(transect_herpetofauna_translocation_db)
    return transect_herpetofauna_translocation_db


# Update transect herpetofauna translocation
async def update_transect_herpetofauna_translocation(
        db: AsyncSession,
        transect_herpetofauna_translocation_id: int,
        transect_herpetofauna_translocation_update: TransectHerpetofaunaTranslocationBase
        ) -> TransectHerpetofaunaTranslocation:
    result = await db.execute(
            select(TransectHerpetofaunaTranslocation)
            .where(
                TransectHerpetofaunaTranslocation.id == transect_herpetofauna_translocation_id
                )
            )
    transect_herpetofauna_translocation_db = result.scalars().first()
    if not transect_herpetofauna_translocation_db:
        raise HTTPException(
                status_code=404,
                detail="Transect herpetofauna translocation not found"
                )
    transect_herpetofauna_translocation_db.cod = transect_herpetofauna_translocation_update.cod
    transect_herpetofauna_translocation_db.date = transect_herpetofauna_translocation_update.date
    transect_herpetofauna_translocation_db.latitude_in = transect_herpetofauna_translocation_update.latitude_in
    transect_herpetofauna_translocation_db.longitude_in = transect_herpetofauna_translocation_update.longitude_in
    transect_herpetofauna_translocation_db.altitude_in = transect_herpetofauna_translocation_update.altitude_in
    transect_herpetofauna_translocation_db.latitude_out = transect_herpetofauna_translocation_update.latitude_out
    transect_herpetofauna_translocation_db.longitude_out = transect_herpetofauna_translocation_update.longitude_out
    transect_herpetofauna_translocation_db.altitude_out = transect_herpetofauna_translocation_update.altitude_out
    await db.commit()
    await db.refresh(transect_herpetofauna_translocation_db)
    return transect_herpetofauna_translocation_db


# Delete transect herpetofauna translocation
async def delete_transect_herpetofauna_translocation(
        db: AsyncSession,
        transect_herpetofauna_translocation_id: int
        ) -> TransectHerpetofaunaTranslocation:
    result = await db.execute(
            select(TransectHerpetofaunaTranslocation)
            .where(
                TransectHerpetofaunaTranslocation.id == transect_herpetofauna_translocation_id
                )
            )
    transect_herpetofauna_translocation_db = result.scalars().first()
    if not transect_herpetofauna_translocation_db:
        raise HTTPException(
                status_code=404,
                detail="Transect herpetofauna translocation not found"
                )
    await db.execute(
            delete(TransectHerpetofaunaTranslocation)
            .where(TransectHerpetofaunaTranslocation.id == transect_herpetofauna_translocation_id
                   )
            )
    await db.commit()
    return transect_herpetofauna_translocation_db

"""
CRUD FOR POINT HERPETOFAUNA TRANSLOCATION
"""


# Get if point herpetofauna translocation exists by cod
async def get_point_herpetofauna_translocation_by_cod(
        db: AsyncSession,
        cod: str) -> PointHerpetofaunaTranslocation | None:
    result = await db.execute(
            select(PointHerpetofaunaTranslocation)
            .where(PointHerpetofaunaTranslocation.cod == cod)
            )
    return result.scalars().first()


# Get point h erpetofauna translocation by id
async def get_point_herpetofauna_translocation_by_id(
        db: AsyncSession,
        id: int
        ) -> PointHerpetofaunaTranslocation | None:
    result = await db.execute(
            select(PointHerpetofaunaTranslocation)
            .where(PointHerpetofaunaTranslocation.id == id)
            )
    return result.scalars().first()


# Get all point herpetofauna translocation
async def get_all_point_herpetofauna_translocation(
        db: AsyncSession
        ) -> List[PointHerpetofaunaTranslocation]:
    point_herpetofauna_translocation_db = await db.execute(
            select(PointHerpetofaunaTranslocation)
            )
    return list(point_herpetofauna_translocation_db.scalars().all())


# Create point herpetofauna translocation
async def create_point_herpetofauna_translocation(
        db: AsyncSession,
        point_herpetofauna_translocation: PointHerpetofaunaTranslocationCreate
        ) -> PointHerpetofaunaTranslocation:
    point_herpetofauna_translocation_db = PointHerpetofaunaTranslocation(
        cod=point_herpetofauna_translocation.cod,
        date=point_herpetofauna_translocation.date,
        latitude=point_herpetofauna_translocation.latitude,
        longitude=point_herpetofauna_translocation.longitude,
        altitude=point_herpetofauna_translocation.altitude,
    )
    db.add(point_herpetofauna_translocation_db)
    await db.commit()
    await db.refresh(point_herpetofauna_translocation_db)
    return point_herpetofauna_translocation_db


# Update point herpetofauna translocation
async def update_point_herpetofauna_translocation(
        db: AsyncSession,
        point_herpetofauna_translocation_id: int,
        point_herpetofauna_translocation_update: PointHerpetofaunaTranslocationBase
        ) -> PointHerpetofaunaTranslocation:
    result = await db.execute(
            select(PointHerpetofaunaTranslocation)
            .where(PointHerpetofaunaTranslocation.id == point_herpetofauna_translocation_id)
            )
    point_herpetofauna_translocation_db = result.scalars().first()
    if not point_herpetofauna_translocation_db:
        raise HTTPException(
                status_code=404,
                detail="Point herpetofauna translocation not found"
                )
    point_herpetofauna_translocation_db.cod = point_herpetofauna_translocation_update.cod
    point_herpetofauna_translocation_db.date = point_herpetofauna_translocation_update.date
    point_herpetofauna_translocation_db.latitude = point_herpetofauna_translocation_update.latitude
    point_herpetofauna_translocation_db.longitude = point_herpetofauna_translocation_update.longitude
    point_herpetofauna_translocation_db.altitude = point_herpetofauna_translocation_update.altitude
    await db.commit()
    await db.refresh(point_herpetofauna_translocation_db)
    return point_herpetofauna_translocation_db


# Delete point herpetofauna translocation
async def delete_point_herpetofauna_translocation(
        db: AsyncSession,
        point_herpetofauna_translocation_id: int
        ) -> PointHerpetofaunaTranslocation:
    result = await db.execute(
            select(PointHerpetofaunaTranslocation)
            .where(
                PointHerpetofaunaTranslocation.id == point_herpetofauna_translocation_id
                )
            )
    point_herpetofauna_translocation_db = result.scalars().first()
    if not point_herpetofauna_translocation_db:
        raise HTTPException(
                status_code=404,
                detail="Point herpetofauna translocation not found"
                )
    await db.execute(
            delete(PointHerpetofaunaTranslocation)
            .where(PointHerpetofaunaTranslocation.id == point_herpetofauna_translocation_id
                   )
            )
    await db.commit()
    return point_herpetofauna_translocation_db

"""
CRUD FOR TRANSLOCATION HERPETOFAUNA
"""


# Get if translocation herpetofauna exists by cod
async def get_translocation_herpetofauna_by_cod(
        db: AsyncSession,
        cod: str
        ) -> TranslocationHerpetofauna | None:
    result = await db.execute(
            select(TranslocationHerpetofauna)
            .where(TranslocationHerpetofauna.cod == cod)
            )
    return result.scalars().first()


# Get translocation herpetofauna by id
async def get_translocation_herpetofauna_by_id(
        db: AsyncSession,
        id: int
        ) -> TranslocationHerpetofauna | None:
    result = await db.execute(
            select(TranslocationHerpetofauna)
            .where(TranslocationHerpetofauna.id == id)
            )
    return result.scalars().first()


# Get all translocation herpetofauna
async def get_all_translocation_herpetofauna(
        db: AsyncSession
        ) -> List[TranslocationHerpetofauna]:
    translocations_hertofauna_db = await db.execute(
            select(TranslocationHerpetofauna)
            )
    return list(translocations_hertofauna_db.scalars().all())


# Create translocation herpetofauna
async def create_translocation_herpetofauna(
        db: AsyncSession,
        translocation_herpetofauna: TranslocationHerpetofaunaCreate,
        ) -> TranslocationHerpetofauna:
    translocation_herpetofauna_db = TranslocationHerpetofauna(
            cod=translocation_herpetofauna.cod,
            transect_herpetofauna_translocation_id=translocation_herpetofauna.transect_herpetofauna_translocation_id,
            point_herpetofauna_translocation_id=translocation_herpetofauna.point_herpetofauna_translocation_id,
            specie_id=translocation_herpetofauna.specie_id,
            mark_herpetofauna_id=translocation_herpetofauna.mark_herpetofauna_id,
        )
    db.add(translocation_herpetofauna_db)
    await db.commit()
    await db.refresh(translocation_herpetofauna_db)
    return translocation_herpetofauna_db


# Update translocation herpetofauna
async def update_translocation_herpetofauna(
        db: AsyncSession,
        translocation_herpetofauna_id: int,
        translocation_herpetofauna_update: TranslocationHerpetofaunaBase
        ) -> TranslocationHerpetofauna:
    result = await db.execute(
            select(TranslocationHerpetofauna).
            where(
                TranslocationHerpetofauna.id == translocation_herpetofauna_id
                )
            )
    translocation_herpetofauna_db = result.scalars().first()
    if not translocation_herpetofauna_db:
        raise HTTPException(
                status_code=404,
                detail="Translocation herpetofauna not found"
                )
    translocation_herpetofauna_db.cod = translocation_herpetofauna_update.cod
    translocation_herpetofauna_db.transect_herpetofauna_translocation_id = translocation_herpetofauna_update.transect_herpetofauna_translocation_id
    translocation_herpetofauna_db.point_herpetofauna_translocation_id = translocation_herpetofauna_update.point_herpetofauna_translocation_id
    translocation_herpetofauna_db.specie_id = translocation_herpetofauna_update.specie_id
    translocation_herpetofauna_db.mark_herpetofauna_id = translocation_herpetofauna_update.mark_herpetofauna_id
    await db.commit()
    await db.refresh(translocation_herpetofauna_db)
    return translocation_herpetofauna_db


# Delete translocation herpetofauna
async def delete_translocation_herpetofauna(
        db: AsyncSession,
        translocation_herpetofauna_id: int
        ) -> TranslocationHerpetofauna:
    result = await db.execute(
            select(TranslocationHerpetofauna)
            .where(
                TranslocationHerpetofauna.id == translocation_herpetofauna_id
                )
            )
    translocation_herpetofauna_db = result.scalars().first()
    if not translocation_herpetofauna_db:
        raise HTTPException(
                status_code=404,
                detail="Translocation herpetofauna not found"
                )
    await db.execute(
            delete(TranslocationHerpetofauna)
            .where(
                TranslocationHerpetofauna.id == translocation_herpetofauna_id
                )
            )
    await db.commit()
    return translocation_herpetofauna_db

"""
CRUD FOR TRANSECT HERPETOFAUNA WIHT SPECIES AND COUNT
"""


# Get transect herpetofauna with species and count by name
async def get_transect_herpetofauna_with_species_and_count_by_name(
        db: AsyncSession
        ) -> List[TransectHerpetoWithSpecies]:
    transectors = await get_all_transect_herpetofauna(db)

    result = []

    for transect in transectors:
        # get rescue id
        result_db = await db.execute(
                select(RescueHerpetofauna)
                .where(
                    RescueHerpetofauna.transect_herpetofauna_id == transect.id
                    ))
        rescue_list = list(result_db.scalars().all())
        species = []
        total_rescue = 0
        for rescue in rescue_list:
            specie_id = rescue.specie_id
            specie = await get_specie_by_id(db, specie_id)
            if specie:
                species.append(specie.specific_epithet)
            total_rescue += 1
        result.append(TransectHerpetoWithSpecies(
            number=transect.number,
            date_in=transect.date_in,
            date_out=transect.date_out,
            latitude_in=transect.latitude_in,
            longitude_in=transect.longitude_in,
            latitude_out=transect.latitude_out,
            longitude_out=transect.longitude_out,
            specie_names=species,
            total_rescue=total_rescue
        ))
    return result


# Get transect herpetofauna with rescues and species by specie id
async def get_transect_herpetofauna_with_rescues_and_species_by_specie_id(
        db: AsyncSession,
        id: int
        ) -> List[TransectHerpetoWithSpecies]:
    transectors = await get_all_transect_herpetofauna(db)

    result = []

    transectors = await get_all_transect_herpetofauna(db)

    result = []

    for transect in transectors:
        # get rescue id
        result_db = await db.execute(
                select(RescueHerpetofauna)
                .where(
                    RescueHerpetofauna.transect_herpetofauna_id == transect.id
                    ))
        rescue_list = list(result_db.scalars().all())
        species = []
        total_rescue = 0
        for rescue in rescue_list:
            specie_id = rescue.specie_id
            if specie_id == id:
                specie = await get_specie_by_id(db, specie_id)
                if specie:
                    species.append(specie.specific_epithet)
                else:
                    raise HTTPException(
                            status_code=404,
                            detail="Specie not found"
                            )
            else:
                continue
            total_rescue += 1
        if total_rescue == 0:
            continue
        else:
            result.append(TransectHerpetoWithSpecies(
                number=transect.number,
                date_in=transect.date_in,
                date_out=transect.date_out,
                latitude_in=transect.latitude_in,
                longitude_in=transect.longitude_in,
                latitude_out=transect.latitude_out,
                longitude_out=transect.longitude_out,
                specie_names=species,
                total_rescue=total_rescue
            ))
    return result


# Get all transect of relocation with species
async def getTransectRelocationWithSpeciesAndCountOfTranslocation(
        db: AsyncSession
        ) -> List[TransectHerpetoTransWithSpecies]:
    transectors = await get_all_transect_herpetofauna_translocation(db)

    result = []

    for transect in transectors:
        # get rescue id
        result_db = await db.execute(
                select(TranslocationHerpetofauna)
                .where(
                    TranslocationHerpetofauna.transect_herpetofauna_translocation_id == transect.id
                    ))
        translocation_list = list(result_db.scalars().all())
        species = []
        total_translocation = 0
        for translocation in translocation_list:
            specie_id = translocation.specie_id
            specie = await get_specie_by_id(db, specie_id)
            if specie:
                species.append(specie.specific_epithet)
            total_translocation += 1
        result.append(TransectHerpetoTransWithSpecies(
            cod=transect.cod,
            date=transect.date,
            latitude_in=transect.latitude_in,
            longitude_in=transect.longitude_in,
            altitude_in=transect.altitude_in,
            latitude_out=transect.latitude_out,
            longitude_out=transect.longitude_out,
            altitude_out=transect.altitude_out,
            specie_names=species,
            total_translocation=total_translocation
        ))
    return result


# Get all point translocation with species
async def getPointRelocaWithSpecies(
        db: AsyncSession
            ) -> List[PointHerpetoTransloWithSpecies]:
    points = await get_all_point_herpetofauna_translocation(db)

    result = []

    for point in points:
        # get rescue id
        result_db = await db.execute(
                select(TranslocationHerpetofauna)
                .where(
                    TranslocationHerpetofauna.point_herpetofauna_translocation_id == point.id
                    ))
        translocation_list = list(result_db.scalars().all())
        species = []
        total_translocation = 0
        for translocation in translocation_list:
            specie_id = translocation.specie_id
            specie = await get_specie_by_id(db, specie_id)
            if specie:
                species.append(specie.specific_epithet)
            total_translocation += 1
        result.append(PointHerpetoTransloWithSpecies(
            cod=point.cod,
            date=point.date,
            latitude=point.latitude,
            longitude=point.longitude,
            altitude=point.altitude,
            specie_names=species,
            total_translocation=total_translocation
        ))
    return result


async def getRescueHerpetoWithSpecie(
        db: AsyncSession,
        number: str
        ) -> RescueHerpetoWithSpecies:
    rescue = await get_rescue_herpetofauna_by_number(db, number)

    if not rescue:
        raise HTTPException(
                status_code=404,
                detail="Rescue not found"
                )

    specie_id = rescue.specie_id
    specie = await get_specie_by_id(db, specie_id)
    if specie:
        specie_name = specie.specific_epithet
    else:
        raise HTTPException(
                status_code=404,
                detail="Specie not found"
                )
    age_group_id = await get_age_group_by_id(db, rescue.age_group_id)
    if age_group_id:
        age_group = age_group_id.name
    else:
        age_group = None
    transect = await get_transect_herpetofauna_by_id(
            db,
            rescue.transect_herpetofauna_id
            )
    if not transect:
        raise HTTPException(
                status_code=404,
                detail="Transect not found"
                )
    gender: str | None = None
    if rescue.gender is True:
        gender = "Macho"
    if rescue.gender is False:
        gender = "Hembra"

    return RescueHerpetoWithSpecies(
        number=rescue.number,
        date_rescue=transect.date_in,
        gender=gender,
        specie_name=specie_name,
        age_group_name=age_group,
        altitude_in=transect.altitude_in,
        latitude_in=transect.latitude_in,
        longitude_in=transect.longitude_in,
        altitude_out=transect.altitude_out,
        latitude_out=transect.latitude_out,
        longitude_out=transect.longitude_out
    )


async def getAllRescuesHerpetoWithSpecies(
        db: AsyncSession
        ) -> List[RescueHerpetoWithSpecies]:
    rescues = await get_all_rescue_herpetofauna(db)

    result = []

    for rescue in rescues:
        specie_id = rescue.specie_id
        specie = await get_specie_by_id(db, specie_id)
        if specie:
            specie_name = specie.specific_epithet
        else:
            raise HTTPException(
                    status_code=404,
                    detail="Specie not found"
                    )
        age_group_id = await get_age_group_by_id(db, rescue.age_group_id)
        if age_group_id:
            age_group = age_group_id.name
        else:
            age_group = None
        transect = await get_transect_herpetofauna_by_id(
                db,
                rescue.transect_herpetofauna_id
                )
        if not transect:
            raise HTTPException(
                    status_code=404,
                    detail="Transect not found"
                    )
        gender: str | None = None
        if rescue.gender is True:
            gender = "Macho"
        if rescue.gender is False:
            gender = "Hembra"

        result.append(RescueHerpetoWithSpecies(
            number=rescue.number,
            date_rescue=transect.date_in,
            gender=gender,
            specie_name=specie_name,
            age_group_name=age_group,
            altitude_in=transect.altitude_in,
            latitude_in=transect.latitude_in,
            longitude_in=transect.longitude_in,
            altitude_out=transect.altitude_out,
            latitude_out=transect.latitude_out,
            longitude_out=transect.longitude_out
        ))
    return result


async def getPointTranslocationAndMarkHerpetoByNumber(
        db: AsyncSession,
        rescue_number: str
        ) -> PointTranslocationHerpetoWithMark | None:
    """
    Get translocation and mark herpetofauna data by rescue number
    """
    rescue = await get_rescue_herpetofauna_by_number(db, rescue_number)

    if not rescue:
        raise HTTPException(
                status_code=404,
                detail="Rescue not found"
                )

    # get mark herpetofauna by rescue id
    mark = await db.execute(
            select(MarkHerpetofauna)
            .where(
                MarkHerpetofauna.rescue_herpetofauna_id == rescue.id
                ))
    mark_db = mark.scalars().first()

    if not mark_db:
        return None

    # get point herpetofauna translocation by mark id
    translocation = await db.execute(
            select(TranslocationHerpetofauna)
            .where(
                TranslocationHerpetofauna.mark_herpetofauna_id == mark_db.id
                ))
    translocation_db = translocation.scalars().first()

    if not translocation_db:
        return None

    point = await db.execute(
            select(PointHerpetofaunaTranslocation)
            .where(
                PointHerpetofaunaTranslocation.id == translocation_db.point_herpetofauna_translocation_id
                ))
    point_db = point.scalars().first()

    if not point_db:
        return None

    return PointTranslocationHerpetoWithMark(
        cod=translocation_db.cod,
        date=point_db.date,
        latitude=point_db.latitude,
        longitude=point_db.longitude,
        altitude=point_db.altitude,
        number_mark=mark_db.number,
        code_mark=mark_db.code,
        LHC=mark_db.LHC,
        weight=mark_db.weight,
        is_photo_mark=mark_db.is_photo_mark,
        is_elastomer_mark=mark_db.is_elastomer_mark
        )


async def getTransectTranslocationAndMarkHerpetoByNumber(
        db: AsyncSession,
        rescue_number: str
        ) -> TransectTranslocationHerpetoWithMark | None:
    """
    Get translocation and mark herpetofauna data by rescue number
    """
    rescue = await get_rescue_herpetofauna_by_number(db, rescue_number)

    if not rescue:
        raise HTTPException(
                status_code=404,
                detail="Rescue not found"
                )

    # get mark herpetofauna by rescue id
    mark = await db.execute(
            select(MarkHerpetofauna)
            .where(
                MarkHerpetofauna.rescue_herpetofauna_id == rescue.id
                ))
    mark_db = mark.scalars().first()

    if not mark_db:
        return None

    # get point herpetofauna translocation by mark id
    translocation = await db.execute(
            select(TranslocationHerpetofauna)
            .where(
                TranslocationHerpetofauna.mark_herpetofauna_id == mark_db.id
                ))
    translocation_db = translocation.scalars().first()

    if not translocation_db:
        return None

    transect = await db.execute(
            select(TransectHerpetofaunaTranslocation)
            .where(
                TransectHerpetofaunaTranslocation.id == translocation_db.transect_herpetofauna_translocation_id
                ))
    transect_db = transect.scalars().first()

    if not transect_db:
        return None

    return TransectTranslocationHerpetoWithMark(
        cod=translocation_db.cod,
        date=transect_db.date,
        latitude_in=transect_db.latitude_in,
        longitude_in=transect_db.longitude_in,
        latitude_out=transect_db.latitude_out,
        longitude_out=transect_db.longitude_out,
        number_mark=mark_db.number,
        code_mark=mark_db.code,
        LHC=mark_db.LHC,
        weight=mark_db.weight,
        is_photo_mark=mark_db.is_photo_mark,
        is_elastomer_mark=mark_db.is_elastomer_mark
        )


async def getTransectTranslocationByNumber(
        db: AsyncSession,
        rescue_number: str
        ) -> List[TransectHerpetofaunaTranslocationBase] | None:
    """
    Get transect translocation data by rescue number
    """

    rescue = await get_rescue_herpetofauna_by_number(db, rescue_number)
    if not rescue:
        raise HTTPException(
                status_code=404,
                detail="Rescue not found"
                )

    translocations_db = await db.execute(
            select(TranslocationHerpetofauna)
            .where(
                TranslocationHerpetofauna.specie_id == rescue.specie_id
                ))

    translocations = list(translocations_db.scalars().all())

    if not translocations:
        return None

    result = []

    for tranlocation in translocations:
        transect = await db.execute(
                select(TransectHerpetofaunaTranslocation)
                .where(
                    TransectHerpetofaunaTranslocation.id == tranlocation.transect_herpetofauna_translocation_id
                    ))
        transect_db = transect.scalars().first()

        if not transect_db:
            continue

        # Is transect already in result list
        if transect_db in result:
            continue

        result.append(TransectHerpetofaunaTranslocationBase(
            cod=transect_db.cod,
            date=transect_db.date,
            latitude_in=transect_db.latitude_in,
            longitude_in=transect_db.longitude_in,
            altitude_in=transect_db.altitude_in,
            latitude_out=transect_db.latitude_out,
            longitude_out=transect_db.longitude_out,
            altitude_out=transect_db.altitude_out
        ))
    return result
