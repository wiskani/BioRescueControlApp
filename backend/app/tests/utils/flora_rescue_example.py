import random
import string
from sqlalchemy.ext.asyncio import AsyncSession
from app.tests.conftest import *
from app.tests.utils.species_example import *
from app.models.rescue_flora import *


# Create a radom rescue_zone
async def create_random_rescue_zone_id(db: AsyncSession)-> int:
    if db is None:
        raise ValueError("db is None")
    result = await db.execute(select(FloraRescueZone))
    db_rescue_zone = result.scalars().first()
    if db_rescue_zone is not None:
        flora_recue_zone_id = db_rescue_zone.id
        return flora_recue_zone_id
    else:
        flora_recue_zone_id = random.randint(1, 1000)
        db_rescue_zone = FloraRescueZone(
            id=flora_recue_zone_id,
            name="".join(random.choices(string.ascii_uppercase, k=10)),
            description="".join(random.choices(string.ascii_uppercase, k=10)),
        )
        db.add(db_rescue_zone)
        await db.commit()
        await db.refresh(db_rescue_zone)
        return flora_recue_zone_id

async def create_random_relocation_zone_id(db:AsyncSession)-> int:
    if db is None:
        raise ValueError("db is None")
    result = await db.execute(select(FloraRelocationZone))
    db_relocation_zone = result.scalars().first()
    if db_relocation_zone is not None:
        flora_relocation_zone_id = db_relocation_zone.id
        return flora_relocation_zone_id
    else:
        flora_relocation_zone_id = random.randint(1, 1000)
        db_relocation_zone = FloraRelocationZone(
            id=flora_relocation_zone_id,
            name="".join(random.choices(string.ascii_uppercase, k=10)),
        )
        db.add(db_relocation_zone)
        await db.commit()
        await db.refresh(db_relocation_zone)
        return flora_relocation_zone_id


async def create_random_flora_rescue_id(db:AsyncSession) -> int:
    SPECIE_ID = loop.run_until_complete(create_specie_id(db))
    if db is None:
        raise ValueError("db is None")
    result = await db.execute(select(FloraRescue))
    db_flora_rescue = result.scalars().first()
    if db_flora_rescue is not None:
        flora_rescue_id = db_flora_rescue.id
        return flora_rescue_id
    else:
        flora_rescue_id = random.randint(1, 1000)
        db_flora_rescue = FloraRescue(
            id=flora_rescue_id,
            epiphyte_number = random.randint(1, 1000),
            rescue_date = datetime.now(),
            rescue_area_latitude = random.uniform(-90, 90),
            rescue_area_longitude = random.uniform(-180, 180),
            substrate = "sustrate_test",
            dap_bryophyte = 10,
            height_bryophyte = 10,
            bryophyte_position = 1,
            growth_habit = "growth_habit_test",
            epiphyte_phenology = "epiphyte_phenology_test",
            health_status_epiphyte = "health_status_epiphyte_test",
            microhabitat = "microhabitat_test",
            other_observations = "other_observations_test",
            specie_bryophyte_id = SPECIE_ID,
            specie_epiphyte_id = SPECIE_ID,
            rescue_zone_id = await create_random_rescue_zone_id(db),
        )
        db.add(db_flora_rescue)
        await db.commit()
        await db.refresh(db_flora_rescue)
        return flora_rescue_id
