from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import HTTPException

from app.schemas.rescue_flora import (
        # Flora rescue zone
        FloraRescueZoneBase,

        # Flora relocation zone
        FloraRelocationZoneBase,

        # Flora rescue
        FloraRescueBase,

        # Plant nursery
        PlantNurseryBase,

        # Flora relocation
        FloraRelocationBase,

        # Flora rescue with specie
        FloraRescueSpecies,

        # Flora relocation with specie
        FloraRelocationWithSpecie
        )


from app.crud.species import (
        get_specie_by_id,
        get_genus_by_id,
        get_family_by_id
)

from app.models.rescue_flora import (
        FloraRescueZone,
        FloraRelocationZone,
        FloraRescue,
        PlantNursery,
        FloraRelocation
        )

# Purpose: CRUD operations for rescue flora
"""
CRUD FOR FLORA RESCUE ZONE
"""


# Get if flora rescue zone exists
async def get_flora_rescue_zone(
        db: AsyncSession,
        flora_rescue_zone_name: str
        ) -> FloraRescueZone | None:
    rescue_zone_db = await db.execute(
            select(FloraRescueZone)
            .filter(FloraRescueZone.name == flora_rescue_zone_name)
            )
    return rescue_zone_db.scalars().first()


# Get flora rescue zone by id
async def get_flora_rescue_zone_by_id(
        db: AsyncSession,
        flora_rescue_zone_id: int
        ) -> FloraRescueZone | None:
    rescue_zone_db = await db.execute(
            select(FloraRescueZone)
            .filter(FloraRescueZone.id == flora_rescue_zone_id)
            )
    return rescue_zone_db.scalars().first()


# Get all flora rescue zones
async def get_all_flora_rescue_zones(
        db: AsyncSession
        ) -> List[FloraRescueZone]:
    rescue_zones_db = await db.execute(select(FloraRescueZone))
    return list(rescue_zones_db.scalars().all())


# Create a new flora rescue zone
async def create_flora_rescue_zone(
        db: AsyncSession,
        flora_rescue_zone: FloraRescueZoneBase
        ) -> FloraRescueZone:
    db_flora_rescue_zone = FloraRescueZone(
            name=flora_rescue_zone.name,
            description=flora_rescue_zone.description,
            )
    db.add(db_flora_rescue_zone)
    await db.commit()
    await db.refresh(db_flora_rescue_zone)
    return db_flora_rescue_zone


# Update a flora rescue zone
async def update_flora_rescue_zone(
        db: AsyncSession,
        flora_rescue_zone_id: int,
        flora_rescue_zone: FloraRescueZoneBase
        ) -> FloraRescueZone:
    result = await db.execute(
            select(FloraRescueZone)
            .filter(FloraRescueZone.id == flora_rescue_zone_id)
            )
    db_flora_rescue_zone = result.scalars().first()
    if not db_flora_rescue_zone:
        raise HTTPException(
                status_code=404,
                detail="Flora rescue zone not found"
                )
    db_flora_rescue_zone.name = flora_rescue_zone.name
    db_flora_rescue_zone.description = flora_rescue_zone.description
    await db.commit()
    await db.refresh(db_flora_rescue_zone)
    return db_flora_rescue_zone


# Delete a flora rescue zone
async def delete_flora_rescue_zone(
        db: AsyncSession,
        flora_rescue_zone_id: int
        ) -> FloraRescueZone:
    result = await db.execute(
            select(FloraRescueZone).filter(
                FloraRescueZone.id == flora_rescue_zone_id
                )
            )
    db_flora_rescue_zone = result.scalars().first()
    if not db_flora_rescue_zone:
        raise HTTPException(
                status_code=404,
                detail="Flora rescue zone not found"
                )
    await db.delete(db_flora_rescue_zone)
    await db.commit()
    return db_flora_rescue_zone

"""
CRUD FOR FLORA RELOCATION ZONE
"""


# Get if flora relocation zone exists
async def get_flora_relocation_zone(
        db: AsyncSession,
        flora_relocation_zone_name: str
        ) -> FloraRelocationZone | None:
    relocation_zone_db = await db.execute(
            select(FloraRelocationZone).filter(
                FloraRelocationZone.name == flora_relocation_zone_name
                )
            )
    return relocation_zone_db.scalars().first()


# Get flora relocation zone by id
async def get_flora_relocation_zone_by_id(
        db: AsyncSession,
        flora_relocation_zone_id: int
        ) -> FloraRelocationZone | None:
    relocation_zone_db = await db.execute(
            select(FloraRelocationZone).filter(
                FloraRelocationZone.id == flora_relocation_zone_id
                )
            )
    return relocation_zone_db.scalars().first()


# Get all flora relocation zones
async def get_all_flora_relocation_zones(
        db: AsyncSession
        ) -> List[FloraRelocationZone]:
    relocation_zones_db = await db.execute(select(FloraRelocationZone))
    return list(relocation_zones_db.scalars().all())


# Create a new flora relocation zone
async def create_flora_relocation_zone(
        db: AsyncSession,
        flora_relocation_zone: FloraRelocationZoneBase
        ) -> FloraRelocationZone:
    db_flora_relocation_zone = FloraRelocationZone(
            name=flora_relocation_zone.name,
            )
    db.add(db_flora_relocation_zone)
    await db.commit()
    await db.refresh(db_flora_relocation_zone)
    return db_flora_relocation_zone


# Update a flora relocation zone
async def update_flora_relocation_zone(
        db: AsyncSession,
        flora_relocation_zone_id: int,
        flora_relocation_zone: FloraRelocationZoneBase
        ) -> FloraRelocationZone:
    result = await db.execute(
            select(FloraRelocationZone).filter(
                FloraRelocationZone.id == flora_relocation_zone_id
                )
            )
    db_flora_relocation_zone = result.scalars().first()
    if not db_flora_relocation_zone:
        raise HTTPException(
                status_code=404,
                detail="Flora relocation zone not found"
                )
    db_flora_relocation_zone.name = flora_relocation_zone.name
    await db.commit()
    await db.refresh(db_flora_relocation_zone)
    return db_flora_relocation_zone


# Delete a flora relocation zone
async def delete_flora_relocation_zone(
        db: AsyncSession,
        flora_relocation_zone_id: int
        ) -> FloraRelocationZone | None:
    result = await db.execute(
            select(FloraRelocationZone).filter(
                FloraRelocationZone.id == flora_relocation_zone_id
                )
            )
    db_flora_relocation_zone = result.scalars().first()
    if not db_flora_relocation_zone:
        raise HTTPException(
                status_code=404,
                detail="Flora relocation zone not found"
                )
    await db.execute(delete(
        FloraRelocationZone).where(
            FloraRelocationZone.id == flora_relocation_zone_id
            )
        )
    await db.commit()
    return db_flora_relocation_zone

"""
CRUD FOR FLORA RESCUE
"""


async def get_flora_rescue(
        db: AsyncSession,
        flora_rescue_epiphyte_number: str
       ) -> FloraRescue | None:
    """Get if flora rescue exists by epiphyte number"""
    flora_resuce_db = await db.execute(
            select(FloraRescue).filter(
                FloraRescue.epiphyte_number == flora_rescue_epiphyte_number
                )
            )
    return flora_resuce_db.scalars().first()


async def get_flora_rescue_by_id(
        db: AsyncSession,
        flora_rescue_id: int
        ) -> FloraRescue | None:
    """Get flora rescue by id"""
    flora_rescue_db = await db.execute(
            select(FloraRescue).filter(FloraRescue.id == flora_rescue_id)
            )
    return flora_rescue_db.scalars().first()


# Get all flora rescues
async def get_all_flora_rescues(db: AsyncSession) -> List[FloraRescue]:
    flora_rescues_db = await db.execute(select(FloraRescue))
    return list(flora_rescues_db.scalars().all())


# Create a new flora rescue
async def create_flora_rescue(
        db: AsyncSession,
        flora_rescue: FloraRescueBase
        ) -> FloraRescue:
    db_flora_rescue = FloraRescue(
            epiphyte_number=flora_rescue.epiphyte_number,
            rescue_date=flora_rescue.rescue_date,
            rescue_area_latitude=flora_rescue.rescue_area_latitude,
            rescue_area_longitude=flora_rescue.rescue_area_longitude,
            substrate=flora_rescue.substrate,
            dap_bryophyte=flora_rescue.dap_bryophyte,
            height_bryophyte=flora_rescue.height_bryophyte,
            bryophyte_position=flora_rescue.bryophyte_position,
            growth_habit=flora_rescue.growth_habit,
            epiphyte_phenology=flora_rescue.epiphyte_phenology,
            health_status_epiphyte=flora_rescue.health_status_epiphyte,
            microhabitat=flora_rescue.microhabitat,
            other_observations=flora_rescue.other_observations,
            is_epiphyte_confirmed=flora_rescue.is_epiphyte_confirmed,
            is_bryophyte_confirmed=flora_rescue.is_bryophyte_confirmed,
            specie_bryophyte_id=flora_rescue.specie_bryophyte_id,
            genus_bryophyte_id=flora_rescue.genus_bryophyte_id,
            family_bryophyte_id=flora_rescue.family_bryophyte_id,
            specie_epiphyte_id=flora_rescue.specie_epiphyte_id,
            genus_epiphyte_id=flora_rescue.genus_epiphyte_id,
            family_epiphyte_id=flora_rescue.family_epiphyte_id,
            rescue_zone_id=flora_rescue.rescue_zone_id,
            )
    db.add(db_flora_rescue)
    await db.commit()
    await db.refresh(db_flora_rescue)
    return db_flora_rescue


# Update a flora rescue
async def update_flora_rescue(
        db: AsyncSession,
        flora_rescue_id: int,
        flora_rescue: FloraRescueBase
        ) -> FloraRescue:
    db_flora_rescue = await get_flora_rescue_by_id(db, flora_rescue_id)

    if not db_flora_rescue:
        raise HTTPException(status_code=404, detail="Flora rescue not found")
    db_flora_rescue.epiphyte_number = flora_rescue.epiphyte_number
    db_flora_rescue.rescue_date = flora_rescue.rescue_date
    db_flora_rescue.rescue_area_latitude = flora_rescue.rescue_area_latitude
    db_flora_rescue.rescue_area_longitude = flora_rescue.rescue_area_longitude
    db_flora_rescue.substrate = flora_rescue.substrate
    db_flora_rescue.dap_bryophyte = flora_rescue.dap_bryophyte
    db_flora_rescue.height_bryophyte = flora_rescue.height_bryophyte
    db_flora_rescue.bryophyte_position = flora_rescue.bryophyte_position
    db_flora_rescue.growth_habit = flora_rescue.growth_habit
    db_flora_rescue.epiphyte_phenology = flora_rescue.epiphyte_phenology
    db_flora_rescue.health_status_epiphyte = flora_rescue.health_status_epiphyte
    db_flora_rescue.microhabitat = flora_rescue.microhabitat
    db_flora_rescue.other_observations = flora_rescue.other_observations
    db_flora_rescue.is_epiphyte_confirmed = flora_rescue.is_epiphyte_confirmed
    db_flora_rescue.is_bryophyte_confirmed = flora_rescue.is_bryophyte_confirmed
    db_flora_rescue.specie_bryophyte_id = flora_rescue.specie_bryophyte_id
    db_flora_rescue.genus_bryophyte_id = flora_rescue.genus_bryophyte_id
    db_flora_rescue.family_bryophyte_id = flora_rescue.family_bryophyte_id
    db_flora_rescue.specie_epiphyte_id = flora_rescue.specie_epiphyte_id
    db_flora_rescue.genus_epiphyte_id = flora_rescue.genus_epiphyte_id
    db_flora_rescue.family_epiphyte_id = flora_rescue.family_epiphyte_id
    db_flora_rescue.rescue_zone_id = flora_rescue.rescue_zone_id
    await db.commit()
    await db.refresh(db_flora_rescue)
    return db_flora_rescue


# Delete a flora rescue
async def delete_flora_rescue(
        db: AsyncSession,
        flora_rescue_id: int
        ) -> FloraRescue | None:
    db_flora_rescue = await get_flora_rescue_by_id(db, flora_rescue_id)
    if not db_flora_rescue:
        raise HTTPException(status_code=404, detail="Flora rescue not found")
    await db.execute(delete(
        FloraRescue).where(
            FloraRescue.id == flora_rescue_id
            )
                     )
    await db.commit()
    return db_flora_rescue

"""
PLANT NURSERY CRUD
"""


# get if plant nursery exists by cod_reg
async def get_plant_nursery(
        db: AsyncSession,
        plant_nursery_cod_reg: str
        ) -> PlantNursery | None:
    plant_nursery_db = await db.execute(
            select(PlantNursery).where(
                PlantNursery.cod_reg == plant_nursery_cod_reg)
            )
    return plant_nursery_db.scalars().first()


# Get plant nursery by id
async def get_plant_nursery_by_id(
        db: AsyncSession,
        plant_nursery_id: int
        ) -> PlantNursery | None:
    plant_nursery_db = await db.execute(
            select(PlantNursery).where(
                PlantNursery.id == plant_nursery_id)
            )
    return plant_nursery_db.scalars().first()


# Get all plant nurseries
async def get_all_plant_nurseries(db: AsyncSession) -> List[PlantNursery]:
    plant_nurseres_db = await db.execute(select(PlantNursery))
    return list(plant_nurseres_db.scalars())


# Create a new plant nursery
async def create_plant_nursery(
        db: AsyncSession,
        plant_nursery: PlantNurseryBase
        ) -> PlantNursery:
    db_plant_nursery = PlantNursery(
            entry_date=plant_nursery.entry_date,
            cod_reg=plant_nursery.cod_reg,
            health_status_epiphyte=plant_nursery.health_status_epiphyte,
            vegetative_state=plant_nursery.vegetative_state,
            flowering_date=plant_nursery.flowering_date,
            treatment_product=plant_nursery.treatment_product,
            is_pruned=plant_nursery.is_pruned,
            is_phytosanitary_treatment=plant_nursery.is_phytosanitary_treatment,
            substrate=plant_nursery.substrate,
            departure_date=plant_nursery.departure_date,
            flora_rescue_id=plant_nursery.flora_rescue_id,
            )
    db.add(db_plant_nursery)
    await db.commit()
    await db.refresh(db_plant_nursery)
    return db_plant_nursery


# Update a plant nursery
async def update_plant_nursery(
        db: AsyncSession,
        plant_nursery_id: int,
        plant_nursery: PlantNurseryBase
        ) -> PlantNursery:
    db_plant_nursery = await get_plant_nursery_by_id(db, plant_nursery_id)
    if not db_plant_nursery:
        raise HTTPException(status_code=404, detail="Plant nursery not found")
    db_plant_nursery.entry_date = plant_nursery.entry_date
    db_plant_nursery.cod_reg = plant_nursery.cod_reg
    db_plant_nursery.health_status_epiphyte = plant_nursery.health_status_epiphyte
    db_plant_nursery.vegetative_state = plant_nursery.vegetative_state
    db_plant_nursery.flowering_date = plant_nursery.flowering_date
    db_plant_nursery.treatment_product = plant_nursery.treatment_product
    db_plant_nursery.is_pruned = plant_nursery.is_pruned
    db_plant_nursery.is_phytosanitary_treatment = plant_nursery.is_phytosanitary_treatment
    db_plant_nursery.substrate = plant_nursery.substrate
    db_plant_nursery.departure_date = plant_nursery.departure_date
    db_plant_nursery.flora_rescue_id = plant_nursery.flora_rescue_id
    await db.commit()
    await db.refresh(db_plant_nursery)
    return db_plant_nursery


# Delete a plant nursery
async def delete_plant_nursery(
        db: AsyncSession,
        plant_nursery_id: int
        ) -> PlantNursery:
    db_plant_nursery = await get_plant_nursery_by_id(db, plant_nursery_id)
    if not db_plant_nursery:
        raise HTTPException(status_code=404, detail="Plant nursery not found")
    await db.execute(
            delete(PlantNursery).where(
                PlantNursery.id == plant_nursery_id)
            )
    await db.commit()
    return db_plant_nursery

"""
FLORA RELOCATION CRUD
"""


# Get if flora relocation exists
async def get_flora_relocation(
        db: AsyncSession,
        flora_relocation_number: str
        ) -> FloraRelocation | None:
    """Get if flora relocation exists by relocation number"""
    flora_relocation_db = await db.execute(
            select(FloraRelocation).where(
                FloraRelocation.relocation_number == flora_relocation_number)
            )
    return flora_relocation_db.scalars().first()


# Get flora relocation by id
async def get_flora_relocation_by_id(
        db: AsyncSession,
        flora_relocation_id: int
        ) -> FloraRelocation | None:
    """Get flora relocation by id"""
    flora_relocation_db = await db.execute(
            select(FloraRelocation).where(
                FloraRelocation.id == flora_relocation_id)
            )
    return flora_relocation_db.scalars().first()


# Get flora relocation by rescue id
async def get_flora_relocation_by_rescue_id(
        db: AsyncSession,
        flora_rescue_id: int
        ) -> FloraRelocation | None:
    """Get flora relocation by rescue id"""
    flora_relocation_db = await db.execute(
            select(FloraRelocation).where(
                FloraRelocation.flora_rescue_id == flora_rescue_id)
            )
    return flora_relocation_db.scalars().first()


# Get all flora relocations
async def get_all_flora_relocations(db: AsyncSession) -> List[FloraRelocation]:
    flora_relocations_db = await db.execute(select(FloraRelocation))
    return list(flora_relocations_db.scalars())


# Create a new flora relocation
async def create_flora_relocation(
        db: AsyncSession,
        flora_relocation: FloraRelocationBase
        ) -> FloraRelocation:
    db_flora_relocation = FloraRelocation(
            relocation_date=flora_relocation.relocation_date,
            relocation_number=flora_relocation.relocation_number,
            size=flora_relocation.size,
            epiphyte_phenology=flora_relocation.epiphyte_phenology,
            johanson_zone=flora_relocation.johanson_zone,
            relocation_position_latitude=flora_relocation.relocation_position_latitude,
            relocation_position_longitude=flora_relocation.relocation_position_longitude,
            relocation_position_altitude=flora_relocation.relocation_position_altitude,
            bryophyte_number=flora_relocation.bryophyte_number,
            dap_bryophyte=flora_relocation.dap_bryophyte,
            height_bryophyte=flora_relocation.height_bryophyte,
            bark_type=flora_relocation.bark_type,
            infested_lianas=flora_relocation.infested_lianas,
            other_observations=flora_relocation.other_observations,
            is_bryophyte_confirmed=flora_relocation.is_bryophyte_confirmed,
            flora_rescue_id=flora_relocation.flora_rescue_id,
            specie_bryophyte_id=flora_relocation.specie_bryophyte_id,
            genus_bryophyte_id=flora_relocation.genus_bryophyte_id,
            family_bryophyte_id=flora_relocation.family_bryophyte_id,
            relocation_zone_id=flora_relocation.relocation_zone_id,
            )
    db.add(db_flora_relocation)
    await db.commit()
    await db.refresh(db_flora_relocation)
    return db_flora_relocation


# Update a flora relocation
async def update_flora_relocation(
        db: AsyncSession,
        flora_relocation_id: int,
        flora_relocation: FloraRelocationBase
        ) -> FloraRelocation:
    db_flora_relocation = await get_flora_relocation_by_id(
            db,
            flora_relocation_id
            )
    if not db_flora_relocation:
        raise HTTPException(
                status_code=404,
                detail="Flora relocation not found"
                )

    db_flora_relocation.relocation_date = flora_relocation.relocation_date
    db_flora_relocation.relocation_number = flora_relocation.relocation_number
    db_flora_relocation.size = flora_relocation.size
    db_flora_relocation.epiphyte_phenology = flora_relocation.epiphyte_phenology
    db_flora_relocation.johanson_zone = flora_relocation.johanson_zone
    db_flora_relocation.relocation_position_latitude = flora_relocation.relocation_position_latitude
    db_flora_relocation.relocation_position_longitude = flora_relocation.relocation_position_longitude
    db_flora_relocation.relocation_position_altitude = flora_relocation.relocation_position_altitude
    db_flora_relocation.bryophyte_number = flora_relocation.bryophyte_number
    db_flora_relocation.dap_bryophyte = flora_relocation.dap_bryophyte
    db_flora_relocation.height_bryophyte = flora_relocation.height_bryophyte
    db_flora_relocation.bark_type = flora_relocation.bark_type
    db_flora_relocation.infested_lianas = flora_relocation.infested_lianas
    db_flora_relocation.other_observations = flora_relocation.other_observations
    db_flora_relocation.is_bryophyte_confirmed = flora_relocation.is_bryophyte_confirmed
    db_flora_relocation.flora_rescue_id = flora_relocation.flora_rescue_id
    db_flora_relocation.specie_bryophyte_id = flora_relocation.specie_bryophyte_id
    db_flora_relocation.genus_bryophyte_id = flora_relocation.genus_bryophyte_id
    db_flora_relocation.family_bryophyte_id = flora_relocation.family_bryophyte_id
    db_flora_relocation.relocation_zone_id = flora_relocation.relocation_zone_id
    await db.commit()
    await db.refresh(db_flora_relocation)
    return db_flora_relocation


# Delete a flora relocation
async def delete_flora_relocation(
        db: AsyncSession,
        flora_relocation_id: int
        ) -> FloraRelocation:
    db_flora_relocation = await get_flora_relocation_by_id(
            db,
            flora_relocation_id
            )
    if not db_flora_relocation:
        raise HTTPException(
                status_code=404,
                detail="Flora relocation not found"
                )
    await db.execute(
            delete(FloraRelocation).where(
                FloraRelocation.id == flora_relocation_id)
            )
    await db.commit()
    return db_flora_relocation

"""
CRUD RESCUE FLORA WITH SPECIE
"""


# Get rescue flora with specie, genus and family name
async def get_rescue_flora_with_specie(
        db: AsyncSession
        ) -> List[FloraRescueSpecies]:
    rescues: list[FloraRescue] = await get_all_flora_rescues(db)

    result = []

    for rescue in rescues:
        specie = None
        genus = None
        family = None

        specie_bryophyte = None
        genus_bryophyte = None
        family_bryophyte = None

        # Construct specie epiphyte
        specie_db = await get_specie_by_id(db, rescue.specie_epiphyte_id)
        if specie_db:
            specie = specie_db.specific_epithet
            genus_db = await get_genus_by_id(db, specie_db.genus_id)
            if genus_db:
                genus = genus_db.genus_name
                family_db = await get_family_by_id(db, genus_db.family_id)
                if family_db:
                    family = family_db.family_name

        genus_db = await get_genus_by_id(db, rescue.genus_epiphyte_id)
        if genus_db:
            genus = genus_db.genus_name
            family_db = await get_family_by_id(db, genus_db.family_id)
            if family_db:
                family = family_db.family_name

        family_db = await get_family_by_id(db, rescue.family_epiphyte_id)
        if family_db:
            family = family_db.family_name

        # Construct specie bryophyte
        specie_bryophyte_db = await get_specie_by_id(
                db,
                rescue.specie_bryophyte_id
                )
        if specie_bryophyte_db:
            specie_bryophyte = specie_bryophyte_db.specific_epithet
            genus_bryophyte_db = await get_genus_by_id(
                    db,
                    specie_bryophyte_db.genus_id
                    )
            if genus_bryophyte_db:
                genus_bryophyte = genus_bryophyte_db.genus_name
                family_bryophyte_db = await get_family_by_id(
                        db,
                        genus_bryophyte_db.family_id
                        )
                if family_bryophyte_db:
                    family_bryophyte = family_bryophyte_db.family_name

        genus_bryophyte_db = await get_genus_by_id(
                db,
                rescue.genus_bryophyte_id
                )
        if genus_bryophyte_db:
            genus_bryophyte = genus_bryophyte_db.genus_name
            family_bryophyte_db = await get_family_by_id(
                    db,
                    genus_bryophyte_db.family_id
                    )
            if family_bryophyte_db:
                family_bryophyte = family_bryophyte_db.family_name

        family_bryophyte_db = await get_family_by_id(
                db,
                rescue.family_bryophyte_id
                )
        if family_bryophyte_db:
            family_bryophyte = family_bryophyte_db.family_name

        result.append(FloraRescueSpecies(
            epiphyte_number=rescue.epiphyte_number,
            rescue_date=rescue.rescue_date,
            rescue_area_latitude=rescue.rescue_area_latitude,
            rescue_area_longitude=rescue.rescue_area_longitude,
            specie_name=specie,
            genus_name=genus,
            family_name=family,
            substrate=rescue.substrate,
            dap_bryophyte=rescue.dap_bryophyte,
            height_bryophyte=rescue.height_bryophyte,
            bryophyte_position=rescue.bryophyte_position,
            growth_habit=rescue.growth_habit,
            epiphyte_phenology=rescue.epiphyte_phenology,
            health_status_epiphyte=rescue.health_status_epiphyte,
            microhabitat=rescue.microhabitat,
            other_observations=rescue.other_observations,
            is_epiphyte_confirmed=rescue.is_epiphyte_confirmed,
            is_bryophyte_confirmed=rescue.is_bryophyte_confirmed,
            specie_bryophyte_name=specie_bryophyte,
            genus_bryophyte_name=genus_bryophyte,
            family_bryophyte_name=family_bryophyte,
            ))

    return result


# Get rescue flora with specie, genus and family name by specie id
async def get_rescue_flora_with_specie_by_specie_id(
        db: AsyncSession,
        specie_id: int
        ) -> List[FloraRescueSpecies]:
    rescues = await db.execute(
            select(FloraRescue).filter(
                FloraRescue.specie_epiphyte_id == specie_id)
            )
    rescues_db = rescues.scalars().all()

    result = []

    for rescue in rescues_db:
        specie_db = await get_specie_by_id(db, rescue.specie_epiphyte_id)
        if specie_db:
            specie = specie_db.specific_epithet
        else:
            specie = None

        genus_db = await get_genus_by_id(db, rescue.genus_epiphyte_id)
        if genus_db:
            genus = genus_db.genus_name
        else:
            genus = None

        family_db = await get_family_by_id(db, rescue.family_epiphyte_id)
        if family_db:
            family = family_db.family_name
        else:
            family = None

        specie_bryophyte_db = await get_specie_by_id(
                db,
                rescue.specie_bryophyte_id
                )
        if specie_bryophyte_db:
            specie_bryophyte = specie_bryophyte_db.specific_epithet
        else:
            specie_bryophyte = None

        genus_bryophyte_db = await get_genus_by_id(
                db,
                rescue.genus_bryophyte_id
                )
        if genus_bryophyte_db:
            genus_bryophyte = genus_bryophyte_db.genus_name
        else:
            genus_bryophyte = None

        family_bryophyte_db = await get_family_by_id(
                db,
                rescue.family_bryophyte_id
                )
        if family_bryophyte_db:
            family_bryophyte = family_bryophyte_db.family_name
        else:
            family_bryophyte = None

        result.append(FloraRescueSpecies(
            epiphyte_number=rescue.epiphyte_number,
            rescue_date=rescue.rescue_date,
            rescue_area_latitude=rescue.rescue_area_latitude,
            rescue_area_longitude=rescue.rescue_area_longitude,
            specie_name=specie,
            genus_name=genus,
            family_name=family,
            substrate=rescue.substrate,
            dap_bryophyte=rescue.dap_bryophyte,
            height_bryophyte=rescue.height_bryophyte,
            bryophyte_position=rescue.bryophyte_position,
            growth_habit=rescue.growth_habit,
            epiphyte_phenology=rescue.epiphyte_phenology,
            health_status_epiphyte=rescue.health_status_epiphyte,
            microhabitat=rescue.microhabitat,
            other_observations=rescue.other_observations,
            is_epiphyte_confirmed=rescue.is_epiphyte_confirmed,
            is_bryophyte_confirmed=rescue.is_bryophyte_confirmed,
            specie_bryophyte_name=specie_bryophyte,
            genus_bryophyte_name=genus_bryophyte,
            family_bryophyte_name=family_bryophyte,
            ))

    return result


# Get all translocation with specie and other data
async def get_all_translocation_with_specie(
        db: AsyncSession
        ) -> List[FloraRelocationWithSpecie] | HTTPException:
    relocations = await get_all_flora_relocations(db)
    if not relocations:
        raise HTTPException(status_code=404, detail="Relocations not found")
    relocation_result = []

    for relocation in relocations:
        rescue_db = await get_flora_rescue_by_id(
                db,
                relocation.flora_rescue_id
                )
        if not rescue_db:
            raise HTTPException(status_code=404, detail="Rescue not found")
        specie_db = await get_specie_by_id(db, rescue_db.specie_epiphyte_id)
        if specie_db:
            specie_epiphyte = specie_db.specific_epithet
        else:
            specie_epiphyte = None

        genus_db = await get_genus_by_id(db, rescue_db.genus_epiphyte_id)
        if genus_db:
            genus_epiphyte = genus_db.genus_name
        else:
            genus_epiphyte = None

        family_db = await get_family_by_id(db, rescue_db.family_epiphyte_id)
        if family_db:
            family_epiphyte = family_db.family_name
        else:
            family_epiphyte = None

        specie_db = await get_specie_by_id(db, relocation.specie_bryophyte_id)
        if specie_db:
            specie_bryophyte = specie_db.specific_epithet
        else:
            specie_bryophyte = None

        genus_db = await get_genus_by_id(db, relocation.genus_bryophyte_id)
        if genus_db:
            genus_bryophyte = genus_db.genus_name
        else:
            genus_bryophyte = None

        family_db = await get_family_by_id(db, relocation.family_bryophyte_id)
        if family_db:
            family_bryophyte = family_db.family_name
        else:
            family_bryophyte = None

        relocation_zone_db = await get_flora_relocation_zone_by_id(
                db,
                relocation.relocation_zone_id
                )
        if not relocation_zone_db:
            raise HTTPException(
                    status_code=404,
                    detail="Relocation zone not found"
                    )
        else:
            relocation_zone = relocation_zone_db.name

        relocation_result.append(FloraRelocationWithSpecie(
            relocation_date=relocation.relocation_date,
            flora_rescue=rescue_db.epiphyte_number,
            specie_name_epiphyte=specie_epiphyte,
            genus_name_epiphyte=genus_epiphyte,
            family_name_epiphyte=family_epiphyte,
            size=relocation.size,
            epiphyte_phenology=relocation.epiphyte_phenology,
            johanson_zone=relocation.johanson_zone,
            relocation_position_latitude=relocation.relocation_position_latitude,
            relocation_position_longitude=relocation.relocation_position_longitude,
            relocation_position_altitude=relocation.relocation_position_altitude,
            dap_bryophyte=relocation.dap_bryophyte,
            height_bryophyte=relocation.height_bryophyte,
            bark_type=relocation.bark_type,
            infested_lianas=relocation.infested_lianas,
            other_observations=relocation.other_observations,
            specie_name_bryophyte=specie_bryophyte,
            genus_name_bryophyte=genus_bryophyte,
            family_name_bryophyte=family_bryophyte,
            relocation_zone=relocation_zone
            ))

    return relocation_result


"""
CRUD FOR FLORA RESCUE AND RELOCATION BY EPYPHYTE NUMBER
"""


async def get_rescue_flora_with_specie_by_epiphyte_number(
        db: AsyncSession,
        epiphyte_number: str
        ) -> FloraRescueSpecies | HTTPException:
    """
    Get rescue flora with specie, genus and family name by epiphyte number
    """
    rescue: FloraRescue = await get_flora_rescue(db, epiphyte_number)
    if not rescue:
        return HTTPException(status_code=404, detail="Rescue not found")

    specie = None
    genus = None
    family = None

    specie_bryophyte = None
    genus_bryophyte = None
    family_bryophyte = None

    # Construct specie epiphyte
    specie_db = await get_specie_by_id(db, rescue.specie_epiphyte_id)
    if specie_db:
        specie = specie_db.specific_epithet
        genus_db = await get_genus_by_id(db, specie_db.genus_id)
        if genus_db:
            genus = genus_db.genus_name
            family_db = await get_family_by_id(db, genus_db.family_id)
            if family_db:
                family = family_db.family_name

    genus_db = await get_genus_by_id(db, rescue.genus_epiphyte_id)
    if genus_db:
        genus = genus_db.genus_name
        family_db = await get_family_by_id(db, genus_db.family_id)
        if family_db:
            family = family_db.family_name

    family_db = await get_family_by_id(db, rescue.family_epiphyte_id)
    if family_db:
        family = family_db.family_name

    # Construct specie bryophyte
    specie_bryophyte_db = await get_specie_by_id(
            db,
            rescue.specie_bryophyte_id
            )
    if specie_bryophyte_db:
        specie_bryophyte = specie_bryophyte_db.specific_epithet
        genus_bryophyte_db = await get_genus_by_id(
                db,
                specie_bryophyte_db.genus_id
                )
        if genus_bryophyte_db:
            genus_bryophyte = genus_bryophyte_db.genus_name
            family_bryophyte_db = await get_family_by_id(
                    db,
                    genus_bryophyte_db.family_id
                    )
            if family_bryophyte_db:
                family_bryophyte = family_bryophyte_db.family_name

    genus_bryophyte_db = await get_genus_by_id(
            db,
            rescue.genus_bryophyte_id
            )
    if genus_bryophyte_db:
        genus_bryophyte = genus_bryophyte_db.genus_name
        family_bryophyte_db = await get_family_by_id(
                db,
                genus_bryophyte_db.family_id
                )
        if family_bryophyte_db:
            family_bryophyte = family_bryophyte_db.family_name

    family_bryophyte_db = await get_family_by_id(
            db,
            rescue.family_bryophyte_id
            )
    if family_bryophyte_db:
        family_bryophyte = family_bryophyte_db.family_name

    return (FloraRescueSpecies(
        epiphyte_number=rescue.epiphyte_number,
        rescue_date=rescue.rescue_date,
        rescue_area_latitude=rescue.rescue_area_latitude,
        rescue_area_longitude=rescue.rescue_area_longitude,
        specie_name=specie,
        genus_name=genus,
        family_name=family,
        substrate=rescue.substrate,
        dap_bryophyte=rescue.dap_bryophyte,
        height_bryophyte=rescue.height_bryophyte,
        bryophyte_position=rescue.bryophyte_position,
        growth_habit=rescue.growth_habit,
        epiphyte_phenology=rescue.epiphyte_phenology,
        health_status_epiphyte=rescue.health_status_epiphyte,
        microhabitat=rescue.microhabitat,
        other_observations=rescue.other_observations,
        is_epiphyte_confirmed=rescue.is_epiphyte_confirmed,
        is_bryophyte_confirmed=rescue.is_bryophyte_confirmed,
        specie_bryophyte_name=specie_bryophyte,
        genus_bryophyte_name=genus_bryophyte,
        family_bryophyte_name=family_bryophyte,
        ))


async def get_translocation_with_specie_by_epiphyte_number(
        db: AsyncSession,
        epiphyte_number: str
        ) -> FloraRelocationWithSpecie | HTTPException | dict:
    """
    Get all translocation with specie and other data by epiphyte number
    """
    specie_epiphyte = None
    genus_epiphyte = None
    family_epiphyte = None

    specie_bryophyte = None
    genus_bryophyte = None
    family_bryophyte = None

    rescue = await get_flora_rescue(db, epiphyte_number)
    if not rescue:
        return HTTPException(status_code=404, detail="Rescue not found")

    specie_db = await get_specie_by_id(db, rescue.specie_epiphyte_id)
    if specie_db:
        specie_epiphyte = specie_db.specific_epithet
        genus_db = await get_genus_by_id(db, specie_db.genus_id)
        if genus_db:
            genus_epiphyte = genus_db.genus_name
            family_db = await get_family_by_id(db, genus_db.family_id)
            if family_db:
                family_epiphyte = family_db.family_name

    genus_db = await get_genus_by_id(db, rescue.genus_epiphyte_id)
    if genus_db:
        genus_epiphyte = genus_db.genus_name
        family_db = await get_family_by_id(db, genus_db.family_id)
        if family_db:
            family_epiphyte = family_db.family_name

    family_db = await get_family_by_id(db, rescue.family_epiphyte_id)
    if family_db:
        family_epiphyte = family_db.family_name

    relocation = await get_flora_relocation_by_rescue_id(db, rescue.id)
    if not relocation:
        return {"message": "Relocation not found"}

    specie_bryopyte_db = await get_specie_by_id(
            db, relocation.specie_bryophyte_id
            )
    if specie_bryopyte_db:
        specie_bryophyte = specie_bryopyte_db.specific_epithet
        genus_bryophyte_db = await get_genus_by_id(
                db,
                specie_bryopyte_db.genus_id
                )
        if genus_bryophyte_db:
            genus_bryophyte = genus_bryophyte_db.genus_name
            family_bryophyte_db = await get_family_by_id(
                    db,
                    genus_bryophyte_db.family_id
                    )
            if family_bryophyte_db:
                family_bryophyte = family_bryophyte_db.family_name

    genus_bryophyte_db = await get_genus_by_id(
            db,
            relocation.genus_bryophyte_id
            )
    if genus_bryophyte_db:
        genus_bryophyte = genus_bryophyte_db.genus_name
        family_bryophyte_db = await get_family_by_id(
                db,
                genus_bryophyte_db.family_id
                )

    family_bryophyte_db = await get_family_by_id(
            db,
            relocation.family_bryophyte_id
            )
    if family_bryophyte_db:
        family_bryophyte = family_bryophyte_db.family_name

    relocation_zone_db = await get_flora_relocation_zone_by_id(
            db,
            relocation.relocation_zone_id
            )
    if not relocation_zone_db:
        raise HTTPException(
                status_code=404,
                detail="Relocation zone not found"
                )
    else:
        relocation_zone = relocation_zone_db.name

    return (FloraRelocationWithSpecie(
        relocation_date=relocation.relocation_date,
        flora_rescue=rescue.epiphyte_number,
        specie_name_epiphyte=specie_epiphyte,
        genus_name_epiphyte=genus_epiphyte,
        family_name_epiphyte=family_epiphyte,
        size=relocation.size,
        epiphyte_phenology=relocation.epiphyte_phenology,
        johanson_zone=relocation.johanson_zone,
        relocation_position_latitude=relocation.relocation_position_latitude,
        relocation_position_longitude=relocation.relocation_position_longitude,
        relocation_position_altitude=relocation.relocation_position_altitude,
        dap_bryophyte=relocation.dap_bryophyte,
        height_bryophyte=relocation.height_bryophyte,
        bark_type=relocation.bark_type,
        infested_lianas=relocation.infested_lianas,
        other_observations=relocation.other_observations,
        specie_name_bryophyte=specie_bryophyte,
        genus_name_bryophyte=genus_bryophyte,
        family_name_bryophyte=family_bryophyte,
        relocation_zone=relocation_zone
        ))
