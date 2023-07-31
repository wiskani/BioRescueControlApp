import random
import string
from app.tests.conftest import *
from app.tests.utils.species_example import *
from app.models.rescue_flora import *

db: Session = next(override_get_db())

# Create a radom rescue_zone
def create_random_rescue_zone_id()-> int:
    db_rescue_zone = db.query(FloraRescueZone).first()
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
        db.commit()
        db.refresh(db_rescue_zone)
        return flora_recue_zone_id

def create_random_relocation_zone_id()-> int:
    db_relocation_zone = db.query(FloraRelocationZone).first()
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
        db.commit()
        db.refresh(db_relocation_zone)
        return flora_relocation_zone_id

def create_random_flora_rescue_id() -> int:
    db_flora_rescue = db.query(FloraRescue).first()
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
            specie_bryophyte_id = create_specie_id(),
            specie_epiphyte_id = create_specie_id(),
            rescue_zone_id = create_random_rescue_zone_id(),
        )
        db.add(db_flora_rescue)
        db.commit()
        db.refresh(db_flora_rescue)
        return flora_rescue_id
