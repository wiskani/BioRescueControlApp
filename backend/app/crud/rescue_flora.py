from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Union
from fastapi import HTTPException
from datetime import date

from app.schemas.rescue_flora import (
        #Flora rescue zone
        FloraRescueZoneBase,
        FloraRescueZoneResponse,

        #Flora relocation zone
        FloraRelocationZoneBase,
        FloraRelocationZoneResponse,

        #Flora rescue
        FloraRescueBase,
        FloraRescueResponse,

        #Plant nursery
        PlantNurseryBase,
        PlantNurseryResponse,

        #Flora relocation
        FloraRelocationBase,
        FloraRelocationResponse,
        )
from app.models.rescue_flora import FloraRescueZone, FloraRelocationZone, FloraRescue, PlantNursery, FloraRelocation

# Purpose: CRUD operations for rescue flora
"""
CRUD FOR FLORA RESCUE ZONE
"""

# Get if flora rescue zone exists 
async def get_flora_rescue_zone(db: AsyncSession, flora_rescue_zone_name: str) -> FloraRescueZone | None:
    rescue_zone_db = await db.execute(select(FloraRescueZone).filter(FloraRescueZone.name == flora_rescue_zone_name))
    return rescue_zone_db.scalars().first()

# Get flora rescue zone by id
async def get_flora_rescue_zone_by_id(db:AsyncSession , flora_rescue_zone_id: int) -> FloraRescueZone |  None:
    rescue_zone_db = await db.execute(select(FloraRescueZone).filter(FloraRescueZone.id == flora_rescue_zone_id))
    return rescue_zone_db.scalars().first()

# Get all flora rescue zones
async def get_all_flora_rescue_zones(db: AsyncSession) -> List[FloraRescueZone]:
    rescue_zones_db = await db.execute(select(FloraRescueZone))
    return list(rescue_zones_db.scalars().all())

# Create a new flora rescue zone
async def create_flora_rescue_zone(db: AsyncSession, flora_rescue_zone: FloraRescueZoneBase) -> FloraRescueZone:
    db_flora_rescue_zone = FloraRescueZone(
            name = flora_rescue_zone.name,
            description = flora_rescue_zone.description,
            )
    db.add(db_flora_rescue_zone)
    await db.commit()
    await db.refresh(db_flora_rescue_zone)
    return db_flora_rescue_zone

# Update a flora rescue zone
async def update_flora_rescue_zone(db: AsyncSession, flora_rescue_zone_id: int, flora_rescue_zone: FloraRescueZoneBase) -> FloraRescueZone:
    result = await db.execute(select(FloraRescueZone).filter(FloraRescueZone.id == flora_rescue_zone_id))
    db_flora_rescue_zone = result.scalars().first()
    if not db_flora_rescue_zone:
        raise HTTPException(status_code=404, detail="Flora rescue zone not found")
    db_flora_rescue_zone.name = flora_rescue_zone.name
    db_flora_rescue_zone.description = flora_rescue_zone.description
    await db.commit()
    await db.refresh(db_flora_rescue_zone)
    return db_flora_rescue_zone

# Delete a flora rescue zone
async def delete_flora_rescue_zone(db: AsyncSession, flora_rescue_zone_id: int) -> FloraRescueZone:
    result = await db.execute(select(FloraRescueZone).filter(FloraRescueZone.id == flora_rescue_zone_id))
    db_flora_rescue_zone = result.scalars().first()
    if not db_flora_rescue_zone:
        raise HTTPException(status_code=404, detail="Flora rescue zone not found")
    await db.delete(db_flora_rescue_zone)
    await db.commit()
    return db_flora_rescue_zone

"""
CRUD FOR FLORA RELOCATION ZONE
"""

# Get if flora relocation zone exists
async def get_flora_relocation_zone(db: AsyncSession, flora_relocation_zone_name: str) -> FloraRelocationZone | None:
    relocation_zone_db = await db.execute(select(FloraRelocationZone).filter(FloraRelocationZone.name == flora_relocation_zone_name))
    return relocation_zone_db.scalars().first()

# Get flora relocation zone by id
async def get_flora_relocation_zone_by_id(db: AsyncSession, flora_relocation_zone_id: int) -> FloraRelocationZone | None:
    relocation_zone_db = await db.execute(select(FloraRelocationZone).filter(FloraRelocationZone.id == flora_relocation_zone_id))
    return relocation_zone_db.scalars().first()

# Get all flora relocation zones
async def get_all_flora_relocation_zones(db: AsyncSession) -> List[FloraRelocationZone]:
    relocation_zones_db = await db.execute(select(FloraRelocationZone))
    return list(relocation_zones_db.scalars().all())

# Create a new flora relocation zone
async def create_flora_relocation_zone(db: AsyncSession, flora_relocation_zone: FloraRelocationZoneBase) -> FloraRelocationZone:
    db_flora_relocation_zone = FloraRelocationZone(
            name = flora_relocation_zone.name,
            )
    db.add(db_flora_relocation_zone)
    await db.commit()
    await db.refresh(db_flora_relocation_zone)
    return db_flora_relocation_zone

# Update a flora relocation zone
async def update_flora_relocation_zone(db: AsyncSession, flora_relocation_zone_id: int, flora_relocation_zone: FloraRelocationZoneBase) -> FloraRelocationZone:
    result = await db.execute(select(FloraRelocationZone).filter(FloraRelocationZone.id == flora_relocation_zone_id))
    db_flora_relocation_zone = result.scalars().first()
    if not db_flora_relocation_zone:
        raise HTTPException(status_code=404, detail="Flora relocation zone not found")
    db_flora_relocation_zone.name = flora_relocation_zone.name
    await db.commit()
    await db.refresh(db_flora_relocation_zone)
    return db_flora_relocation_zone

# Delete a flora relocation zone
async def delete_flora_relocation_zone(db: AsyncSession, flora_relocation_zone_id: int) -> FloraRelocationZone | None:
    result = await db.execute(select(FloraRelocationZone).filter(FloraRelocationZone.id == flora_relocation_zone_id))
    db_flora_relocation_zone = result.scalars().first()
    if not db_flora_relocation_zone:
        raise HTTPException(status_code=404, detail="Flora relocation zone not found")
    await db.execute(delete(FloraRelocationZone).where(FloraRelocationZone.id == flora_relocation_zone_id))
    await db.commit()
    return db_flora_relocation_zone

"""
CRUD FOR FLORA RESCUE
"""

# Get if flora rescue exists by epiphyte number
async def get_flora_rescue(db: AsyncSession, flora_rescue_epiphyte_number: str ) -> FloraRescue | None:
    flora_resuce_db= await db.execute(select(FloraRescue).filter(FloraRescue.epiphyte_number == flora_rescue_epiphyte_number))
    return flora_resuce_db.scalars().first()

# Get flora rescue by id
async def get_flora_rescue_by_id(db: AsyncSession, flora_rescue_id: int) -> FloraRescue | None:
    flora_rescue_db = await db.execute(select(FloraRescue).filter(FloraRescue.id == flora_rescue_id))
    return flora_rescue_db.scalars().first()

# Get all flora rescues
async def get_all_flora_rescues(db: AsyncSession) -> List[FloraRescue]:
    flora_rescues_db = await db.execute(select(FloraRescue))
    return list(flora_rescues_db.scalars().all())

# Create a new flora rescue
async def create_flora_rescue(db: AsyncSession, flora_rescue: FloraRescueBase) -> FloraRescue:
    db_flora_rescue = FloraRescue(
            epiphyte_number = flora_rescue.epiphyte_number,
            rescue_date = flora_rescue.rescue_date,
            rescue_area_latitude = flora_rescue.rescue_area_latitude,
            rescue_area_longitude = flora_rescue.rescue_area_longitude,
            substrate = flora_rescue.substrate,
            dap_bryophyte = flora_rescue.dap_bryophyte,
            height_bryophyte = flora_rescue.height_bryophyte,
            bryophyte_position = flora_rescue.bryophyte_position,
            growth_habit = flora_rescue.growth_habit,
            epiphyte_phenology = flora_rescue.epiphyte_phenology,
            health_status_epiphyte = flora_rescue.health_status_epiphyte,
            microhabitat = flora_rescue.microhabitat,
            other_observations = flora_rescue.other_observations,
            specie_bryophyte_id = flora_rescue.specie_bryophyte_id,
            genus_bryophyte_id = flora_rescue.genus_bryophyte_id,
            family_bryophyte_id = flora_rescue.family_bryophyte_id,
            specie_epiphyte_id = flora_rescue.specie_epiphyte_id,
            genus_epiphyte_id = flora_rescue.genus_epiphyte_id,
            family_epiphyte_id = flora_rescue.family_epiphyte_id,
            rescue_zone_id = flora_rescue.rescue_zone_id,
            )
    db.add(db_flora_rescue)
    await db.commit()
    await db.refresh(db_flora_rescue)
    return db_flora_rescue

# Update a flora rescue
async def update_flora_rescue(db: AsyncSession, flora_rescue_id: int, flora_rescue: FloraRescueBase) -> FloraRescue:
    db_flora_rescue =  await get_flora_rescue_by_id(db, flora_rescue_id)

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
async def delete_flora_rescue(db: AsyncSession, flora_rescue_id: int) -> FloraRescue | None:
    db_flora_rescue =  await get_flora_rescue_by_id(db, flora_rescue_id)
    if not db_flora_rescue:
        raise HTTPException(status_code=404, detail="Flora rescue not found")
    await db.execute(delete(FloraRescue).where(FloraRescue.id == flora_rescue_id))
    await db.commit()
    return db_flora_rescue

"""
PLANT NURSERY CRUD
"""

#get if plant nursery exists by cod_reg
async def get_plant_nursery(db: AsyncSession, plant_nursery_cod_reg:str) -> PlantNursery | None:
    plant_nursery_db = await db.execute(select(PlantNursery).where(PlantNursery.cod_reg == plant_nursery_cod_reg))
    return plant_nursery_db.scalars().first()

# Get plant nursery by id
async def get_plant_nursery_by_id(db: AsyncSession, plant_nursery_id: int) -> PlantNursery | None:
    plant_nursery_db = await db.execute(select(PlantNursery).where(PlantNursery.id == plant_nursery_id))
    return plant_nursery_db.scalars().first()

# Get all plant nurseries
async def get_all_plant_nurseries(db: AsyncSession) -> List[PlantNursery]:
    plant_nurseres_db = await db.execute(select(PlantNursery))
    return list(plant_nurseres_db.scalars())

# Create a new plant nursery
async def create_plant_nursery(db: AsyncSession, plant_nursery: PlantNurseryBase) -> PlantNursery:
    db_plant_nursery = PlantNursery(
            entry_date = plant_nursery.entry_date,
            cod_reg = plant_nursery.cod_reg,
            health_status_epiphyte = plant_nursery.health_status_epiphyte,
            vegetative_state = plant_nursery.vegetative_state,
            flowering_date = plant_nursery.flowering_date,
            treatment_product = plant_nursery.treatment_product,
            is_pruned = plant_nursery.is_pruned,
            is_phytosanitary_treatment = plant_nursery.is_phytosanitary_treatment,
            substrate = plant_nursery.substrate,
            departure_date = plant_nursery.departure_date,
            flora_rescue_id = plant_nursery.flora_rescue_id,
            )
    db.add(db_plant_nursery)
    await db.commit()
    await db.refresh(db_plant_nursery)
    return db_plant_nursery

# Update a plant nursery
async def update_plant_nursery(db: AsyncSession, plant_nursery_id: int, plant_nursery: PlantNurseryBase) -> PlantNursery:
    db_plant_nursery =  await get_plant_nursery_by_id(db, plant_nursery_id)
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
async def delete_plant_nursery(db: AsyncSession, plant_nursery_id: int) -> PlantNursery:
    db_plant_nursery =  await get_plant_nursery_by_id(db, plant_nursery_id)
    if not db_plant_nursery:
        raise HTTPException(status_code=404, detail="Plant nursery not found")
    await db.execute(delete(PlantNursery).where(PlantNursery.id == plant_nursery_id))
    await db.commit()
    return db_plant_nursery

"""
FLORA RELOCATION CRUD
"""

# Get if flora relocation exists
async def get_flora_relocation(db: AsyncSession, flora_relocation_number: int) -> FloraRelocation | None:
    flora_relocation_db = await db.execute(select(FloraRelocation).where(FloraRelocation.relocation_number == flora_relocation_number))
    return flora_relocation_db.scalars().first()

# Get flora relocation by id
async def get_flora_relocation_by_id(db: AsyncSession, flora_relocation_id: int) -> FloraRelocation | None:
    flora_relocation_db = await db.execute(select(FloraRelocation).where(FloraRelocation.id == flora_relocation_id))
    return flora_relocation_db.scalars().first()

# Get all flora relocations
async def get_all_flora_relocations(db: AsyncSession) -> List[FloraRelocation]:
    flora_relocations_db = await db.execute(select(FloraRelocation))
    return list(flora_relocations_db.scalars())

# Create a new flora relocation
async def create_flora_relocation(db: AsyncSession, flora_relocation: FloraRelocationBase) -> FloraRelocation:
    db_flora_relocation = FloraRelocation(
            relocation_date = flora_relocation.relocation_date,
            size = flora_relocation.size,
            epiphyte_phenology = flora_relocation.epiphyte_phenology,
            johanson_zone = flora_relocation.johanson_zone,
            relocation_position_latitude = flora_relocation.relocation_position_latitude,
            relocation_position_longitude = flora_relocation.relocation_position_longitude,
            bryophyte_number = flora_relocation.bryophyte_number,
            dap_bryophyte = flora_relocation.dap_bryophyte,
            height_bryophyte = flora_relocation.height_bryophyte,
            bark_type = flora_relocation.bark_type,
            infested_lianas = flora_relocation.infested_lianas,
            relocation_number = flora_relocation.relocation_number,
            other_observations = flora_relocation.other_observations,
            flora_rescue_id = flora_relocation.flora_rescue_id,
            specie_bryophyte_id = flora_relocation.specie_bryophyte_id,
            genus_bryophyte_id = flora_relocation.genus_bryophyte_id,
            family_bryophyte_id = flora_relocation.family_bryophyte_id,
            relocation_zone_id = flora_relocation.relocation_zone_id,
            )
    db.add(db_flora_relocation)
    await db.commit()
    await db.refresh(db_flora_relocation)
    return db_flora_relocation

# Update a flora relocation
async def update_flora_relocation(db: AsyncSession, flora_relocation_id: int, flora_relocation: FloraRelocationBase) -> FloraRelocation:
    db_flora_relocation = await get_flora_relocation_by_id(db, flora_relocation_id)
    if not db_flora_relocation:
        raise HTTPException(status_code=404, detail="Flora relocation not found")

    db_flora_relocation.relocation_date = flora_relocation.relocation_date
    db_flora_relocation.size = flora_relocation.size
    db_flora_relocation.epiphyte_phenology = flora_relocation.epiphyte_phenology
    db_flora_relocation.johanson_zone = flora_relocation.johanson_zone
    db_flora_relocation.relocation_position_latitude = flora_relocation.relocation_position_latitude
    db_flora_relocation.relocation_position_longitude = flora_relocation.relocation_position_longitude
    db_flora_relocation.bryophyte_number = flora_relocation.bryophyte_number
    db_flora_relocation.dap_bryophyte = flora_relocation.dap_bryophyte
    db_flora_relocation.height_bryophyte = flora_relocation.height_bryophyte
    db_flora_relocation.bark_type = flora_relocation.bark_type
    db_flora_relocation.infested_lianas = flora_relocation.infested_lianas
    db_flora_relocation.relocation_number = flora_relocation.relocation_number
    db_flora_relocation.other_observations = flora_relocation.other_observations
    db_flora_relocation.flora_rescue_id = flora_relocation.flora_rescue_id
    db_flora_relocation.specie_bryophyte_id = flora_relocation.specie_bryophyte_id
    db_flora_relocation.genus_bryophyte_id = flora_relocation.genus_bryophyte_id
    db_flora_relocation.family_bryophyte_id = flora_relocation.family_bryophyte_id
    db_flora_relocation.relocation_zone_id = flora_relocation.relocation_zone_id
    await db.commit()
    await db.refresh(db_flora_relocation)
    return db_flora_relocation

# Delete a flora relocation
async def delete_flora_relocation(db: AsyncSession, flora_relocation_id: int) -> FloraRelocation:
    db_flora_relocation = await get_flora_relocation_by_id(db, flora_relocation_id)
    if not db_flora_relocation:
        raise HTTPException(status_code=404, detail="Flora relocation not found")
    await db.execute(delete(FloraRelocation).where(FloraRelocation.id == flora_relocation_id))
    await db.commit()
    return db_flora_relocation




