import random
from datetime import datetime
from typing import Dict, Any
from sqlalchemy.orm import Session

from app.tests.conftest import *
from app.tests.utils.species_example import *
from app.tests.utils.flora_rescue_example import *
from app.models.rescue_flora import FloraRescueZone, FloraRelocationZone, FloraRescue, FloraRelocation, PlantNursery


#db: Session = next(override_get_db())
#
#SPECIE_ID =  create_specie_id()
#RESCUE_ZONE_ID = create_random_rescue_zone_id()
#RELOCATION_ZONE_ID = create_random_relocation_zone_id()
#FLORA_RESCUE_ID = create_random_flora_rescue_id()
#
#
#
##test for relationships between flora rescue zone and flora_rescue
#def test_flora_rescue_zone_relationships() -> None:
#    #create a rescue zone
#    response = client.post(
#        "/api/rescue_flora/rescue_zone/", json={
#            "name": "test_rescue_zone_100",
#            "description": "test_description",
#            "longitude": -65.000,
#            "latitude": -17.000,
#        },
#    )
#    assert response.status_code == 201, response.text
#    data = response.json()
#    rescue_zone_id = data["id"]
#
#    #create a flora rescue 1
#    response = client.post(
#        "/api/rescue_flora", json={
#            "epiphyte_number": 100,
#            "rescue_date": "2021-10-10T00:00:00",
#            "rescue_area_latitude": -17.001,
#            "rescue_area_longitude": -65.001,
#            "substrate": "test_substrate",
#            "dap_bryophyte": 1.0,
#            "height_bryophyte": 1.0,
#            "bryophyte_position": 1,
#            "growth_habit": "test_growth_habit",
#            "epiphyte_phenology": "test_epiphyte_phenology",
#            "health_status_epiphyte": "test_health_status_epiphyte",
#            "microhabitat": "test_microhabitat",
#            "other_observations": "test_other_observations",
#            "specie_bryophyte_id": SPECIE_ID,
#            "specie_epiphyte_id": SPECIE_ID,
#            "rescue_zone_id": rescue_zone_id,
#        },
#    )
#    assert response.status_code == 201, response.text
#
#    #create a flora rescue 2
#    response = client.post(
#        "/api/rescue_flora", json={
#            "epiphyte_number": 101,
#            "rescue_date": "2021-10-10T00:00:00",
#            "rescue_area_latitude": -17.002,
#            "rescue_area_longitude": -65.002,
#            "substrate": "test_substrate",
#            "dap_bryophyte": 1.0,
#            "height_bryophyte": 1.0,
#            "bryophyte_position": 1,
#            "growth_habit": "test_growth_habit",
#            "epiphyte_phenology": "test_epiphyte_phenology",
#            "health_status_epiphyte": "test_health_status_epiphyte",
#            "microhabitat": "test_microhabitat",
#            "other_observations": "test_other_observations",
#            "specie_bryophyte_id": SPECIE_ID,
#            "specie_epiphyte_id": SPECIE_ID,
#            "rescue_zone_id": rescue_zone_id,
#        },
#    )
#    assert response.status_code == 201, response.text
#
#    #Make a query to data base to get flora_rescue with the same rescue_zone_id
#    flora_rescue = db.query(FloraRescue).filter(FloraRescue.rescue_zone_id == rescue_zone_id).all()
#
#    #Create a list of dictionaries with data
#    flora_resuce_data = [
#        {
#            "epiphyte_number": s.epiphyte_number,
#            "rescue_date": s.rescue_date,
#            "rescue_area_latitude": s.rescue_area_latitude,
#            "rescue_area_longitude": s.rescue_area_longitude,
#            "substrate": s.substrate,
#            "dap_bryophyte": s.dap_bryophyte,
#            "height_bryophyte": s.height_bryophyte,
#            "bryophyte_position": s.bryophyte_position,
#            "growth_habit": s.growth_habit,
#            "epiphyte_phenology": s.epiphyte_phenology,
#            "health_status_epiphyte": s.health_status_epiphyte,
#            "microhabitat": s.microhabitat,
#            "other_observations": s.other_observations,
#            "specie_bryophyte_id": s.specie_bryophyte_id,
#            "specie_epiphyte_id": s.specie_epiphyte_id,
#            "rescue_zone_id": s.rescue_zone_id,
#        }
#        for s in flora_rescue
#    ]
#
#    expected_data = [
#        {
#            "epiphyte_number": 100,
#            "rescue_date": datetime(2021, 10, 10, 0, 0),
#            "rescue_area_latitude": -17.001,
#            "rescue_area_longitude": -65.001,
#            "substrate": "test_substrate",
#            "dap_bryophyte": 1.0,
#            "height_bryophyte": 1.0,
#            "bryophyte_position": 1,
#            "growth_habit": "test_growth_habit",
#            "epiphyte_phenology": "test_epiphyte_phenology",
#            "health_status_epiphyte": "test_health_status_epiphyte",
#            "microhabitat": "test_microhabitat",
#            "other_observations": "test_other_observations",
#            "specie_bryophyte_id": SPECIE_ID,
#            "specie_epiphyte_id": SPECIE_ID,
#            "rescue_zone_id": rescue_zone_id,
#        },
#        {
#            "epiphyte_number": 101,
#            "rescue_date": datetime(2021, 10, 10, 0, 0),
#            "rescue_area_latitude": -17.002,
#            "rescue_area_longitude": -65.002,
#            "substrate": "test_substrate",
#            "dap_bryophyte": 1.0,
#            "height_bryophyte": 1.0,
#            "bryophyte_position": 1,
#            "growth_habit": "test_growth_habit",
#            "epiphyte_phenology": "test_epiphyte_phenology",
#            "health_status_epiphyte": "test_health_status_epiphyte",
#            "microhabitat": "test_microhabitat",
#            "other_observations": "test_other_observations",
#            "specie_bryophyte_id": SPECIE_ID,
#            "specie_epiphyte_id": SPECIE_ID,
#            "rescue_zone_id": rescue_zone_id,
#        },
#    ]
#
#    #Compare the data
#    assert flora_resuce_data == expected_data
#
#
#
#
