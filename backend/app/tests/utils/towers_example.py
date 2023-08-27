import random
import string
from app.tests.conftest import *
from app.models.towers import Tower


db: Session = next(override_get_db())

#Create a tower
def create_random_tower():
    tower = Tower(
        number=random.randint(1, 100),
        latitude=random.uniform(-90, 90),
        longitude=random.uniform(-180, 180)
    )
    db.add(tower)
    db.commit()
    db.refresh(tower)
    return tower
