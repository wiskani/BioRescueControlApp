import random
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.tests.conftest import *
from app.models.towers import Tower

#Create a tower
async def create_random_tower(db:AsyncSession) -> Tower:
    if db is None:
        raise ValueError("db is None")

    else:
        result = await db.execute(select(Tower))
        tower_db  = result.scalars().first()
        if tower_db is not None:
            return tower_db
        else:
            tower_id = random.randint(1, 100)
            tower = Tower(
                id=tower_id,
                number=random.randint(1, 100),
                latitude=random.uniform(-90, 90),
                longitude=random.uniform(-180, 180)
            )
            db.add(tower)
            await db.commit()
            await db.refresh(tower)
            return tower
