import random
from app.tests.conftest import *
from app.models.towers import Tower


db: Session = next(override_get_db())

#Create a tower
def create_random_tower() -> Tower:
    tower_db  = db.query(Tower).first()
    if tower_db is not None:
        tower_id = tower_db.id
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
        db.commit()
        db.refresh(tower)
        return tower
