import random
from datetime import datetime
from typing import Dict, Any
from sqlalchemy.orm import Session

from app.tests.conftest import *
from app.models.rescue_flora import FloraRescueZone, FloraRelocationZone, FloraRescue, FloraRelocation, PlantNursery

db: Session = next(override_get_db())


#test for relationships between flora rescue zone and flora_rescue
def test_flora_rescue_zone_relationships() -> None:
    #create a rescue zone
    response = client.post(
        "/api/rescue_flora/rescue_zone/", json={
            "name": "test_rescue_zone_100",
            "description": "test_description",
            "longitude": -65.000,
            "latitude": -17.000,
        },
    )
    assert response.status_code == 201, response.text
    data = response.json()
    rescue_zone_id = data["id"]

    #create a flora rescue 1
    response = client.post(
        "/api/rescue_flora", json={
            "epiphyte_number": 100,
            "rescue_date": "2021-10-10T00:00:00",
            "rescue_area_latitude": -17.001,
            "rescue_area_longitude": -65.001,
            "dap_bryophyte": 1.0,
            "height_bryophyte": 1.0,
            "bryophyte_position": 1,
            "growth_habit": "test_growth_habit",
            "epiphyte_phenology": "test_epiphyte_phenology",
            "health_status_epiphyte": "test_health_status_epiphyte",
            "microhabitat": "test_microhabitat",
            "other_observations": "test_other_observations",
            "specie_bryophyte_id": 1,
            "specie_epiphyte_id": 1,
            "rescue_zone_id": rescue_zone_id,
        },
    )
    assert response.status_code == 201, response.text

    #create a flora rescue 2
    response = client.post(
        "/api/rescue_flora", json={
            "epiphyte_number": 101,
            "rescue_date": "2021-10-10T00:00:00",
            "rescue_area_latitude": -17.002,
            "rescue_area_longitude": -65.002,
            "dap_bryophyte": 1.0,
            "height_bryophyte": 1.0,
            "bryophyte_position": 1,
            "growth_habit": "test_growth_habit",
            "epiphyte_phenology": "test_epiphyte_phenology",
            "health_status_epiphyte": "test_health_status_epiphyte",
            "microhabitat": "test_microhabitat",
            "other_observations": "test_other_observations",
            "specie_bryophyte_id": 1,
            "specie_epiphyte_id": 1,
            "rescue_zone_id": rescue_zone_id,
        },
    )
    assert response.status_code == 201, response.text

    #Make a query to data base to get flora_rescue with the same rescue_zone_id
    flora_rescue = db.query(FloraRescue).filter(FloraRescue.rescue_zone_id == rescue_zone_id).all()

    #Create a list of dictionaries with data
    flora_resuce_data = [
        {
            "epiphyte_number": s.epiphyte_number,
            "rescue_date": s.rescue_date,
            "rescue_area_latitude": s.rescue_area_latitude,
            "rescue_area_longitude": s.rescue_area_longitude,
            "dap_bryophyte": s.dap_bryophyte,
            "height_bryophyte": s.height_bryophyte,
            "bryophyte_position": s.bryophyte_position,
            "growth_habit": s.growth_habit,
            "epiphyte_phenology": s.epiphyte_phenology,
            "health_status_epiphyte": s.health_status_epiphyte,
            "microhabitat": s.microhabitat,
            "other_observations": s.other_observations,
            "specie_bryophyte_id": s.specie_bryophyte_id,
            "specie_epiphyte_id": s.specie_epiphyte_id,
            "rescue_zone_id": s.rescue_zone_id,
        }
        for s in flora_rescue
    ]

    expected_data = [
        {
            "epiphyte_number": 100,
            "rescue_date": datetime(2021, 10, 10, 0, 0),
            "rescue_area_latitude": -17.001,
            "rescue_area_longitude": -65.001,
            "dap_bryophyte": 1.0,
            "height_bryophyte": 1.0,
            "bryophyte_position": 1,
            "growth_habit": "test_growth_habit",
            "epiphyte_phenology": "test_epiphyte_phenology",
            "health_status_epiphyte": "test_health_status_epiphyte",
            "microhabitat": "test_microhabitat",
            "other_observations": "test_other_observations",
            "specie_bryophyte_id": 1,
            "specie_epiphyte_id": 1,
            "rescue_zone_id": rescue_zone_id,
        },
        {
            "epiphyte_number": 101,
            "rescue_date": datetime(2021, 10, 10, 0, 0),
            "rescue_area_latitude": -17.002,
            "rescue_area_longitude": -65.002,
            "dap_bryophyte": 1.0,
            "height_bryophyte": 1.0,
            "bryophyte_position": 1,
            "growth_habit": "test_growth_habit",
            "epiphyte_phenology": "test_epiphyte_phenology",
            "health_status_epiphyte": "test_health_status_epiphyte",
            "microhabitat": "test_microhabitat",
            "other_observations": "test_other_observations",
            "specie_bryophyte_id": 1,
            "specie_epiphyte_id": 1,
            "rescue_zone_id": rescue_zone_id,
        },
    ]

    #Compare the data
    assert flora_resuce_data == expected_data

#test for relationship between rescue_zone and plant_nursery
def test_rescue_zone_plant_nursery_relationship():
    #create a rescue zone
    response = client.post(
        "/api/rescue_flora/rescue_zone/", json={
            "name": "test_rescue_zone_101",
            "description": "test_description",
            "longitude": -65.000,
            "latitude": -17.000,
        },
    )
    assert response.status_code == 201, response.text
    data = response.json()
    rescue_zone_id = data["id"]

    #create a plant nursery 1
    response = client.post(
        "/api/rescue_flora/plant_nursery", json={
            "entry_date": "2021-12-10T00:00:00",
            "cod_reg": "101",
            "health_status_epiphyte": "test_health_status_epiphyte10",
            "flowering_date": "2021-12-10T00:00:00",
            "vegetative_state": "test_vegetative_state10",
            "treatment_product": "test_treatment_product10",
            "is_pruned": False,
            "is_phytosanitary_treatment": False,
            "substrate": "test_substrate10",
            "departure_date": "2021-12-10T00:00:00",
            "rescue_zone_id": rescue_zone_id,
            "flora_rescue_id": 10,
            "specie_id": 10,
            "relocation_zone_id": 10,
        },
    )
    assert response.status_code == 201, response.text

    #create a plant nursery 2
    response = client.post(
        "/api/rescue_flora/plant_nursery", json={
            "entry_date": "2021-12-10T00:00:00",
            "cod_reg": "102",
            "health_status_epiphyte": "test_health_status_epiphyte10",
            "flowering_date": "2021-12-10T00:00:00",
            "vegetative_state": "test_vegetative_state10",
            "treatment_product": "test_treatment_product10",
            "is_pruned": False,
            "is_phytosanitary_treatment": False,
            "substrate": "test_substrate12",
            "departure_date": "2021-12-10T00:00:00",
            "rescue_zone_id": rescue_zone_id,
            "flora_rescue_id": 12,
            "specie_id": 12,
            "relocation_zone_id": 12,
        },
    )
    assert response.status_code == 201, response.text
    #Make a query to data base to get plant_nursery with the same rescue_zone_id
    plant_nursery = db.query(PlantNursery).filter(PlantNursery.rescue_zone_id == rescue_zone_id).all()

    #Create a list of dictionaries with data
    plant_nursery_data = [
        {
            "entry_date": s.entry_date,
            "cod_reg": s.cod_reg,
            "health_status_epiphyte": s.health_status_epiphyte,
            "flowering_date": s.flowering_date,
            "vegetative_state": s.vegetative_state,
            "treatment_product": s.treatment_product,
            "is_pruned": s.is_pruned,
            "is_phytosanitary_treatment": s.is_phytosanitary_treatment,
            "substrate": s.substrate,
            "departure_date": s.departure_date,
            "rescue_zone_id": s.rescue_zone_id,
            "flora_rescue_id": s.flora_rescue_id,
            "specie_id": s.specie_id,
            "relocation_zone_id": s.relocation_zone_id,
        }
        for s in plant_nursery
    ]

    expected_data = [
        {
            "entry_date": datetime(2021, 12, 10, 0, 0),
            "cod_reg": "101",
            "health_status_epiphyte": "test_health_status_epiphyte10",
            "flowering_date": datetime(2021, 12, 10, 0, 0),
            "vegetative_state": "test_vegetative_state10",
            "treatment_product": "test_treatment_product10",
            "is_pruned": False,
            "is_phytosanitary_treatment": False,
            "substrate": "test_substrate10",
            "departure_date": datetime(2021, 12, 10, 0, 0),
            "rescue_zone_id": rescue_zone_id,
            "flora_rescue_id": 10,
            "specie_id": 10,
            "relocation_zone_id": 10,
        },
        {
            "entry_date": datetime(2021, 12, 10, 0, 0),
            "cod_reg": "102",
            "health_status_epiphyte": "test_health_status_epiphyte10",
            "flowering_date": datetime(2021, 12, 10, 0, 0),
            "vegetative_state": "test_vegetative_state10",
            "treatment_product": "test_treatment_product10",
            "is_pruned": False,
            "is_phytosanitary_treatment": False,
            "substrate": "test_substrate12",
            "departure_date": datetime(2021, 12, 10, 0, 0),
            "rescue_zone_id": rescue_zone_id,
            "flora_rescue_id": 12,
            "specie_id": 12,
            "relocation_zone_id": 12,
        }
    ]

    #Compare the data
    assert plant_nursery_data == expected_data

#test for relationship between rescue_zone and flora_relocation
def test_rescue_zone_flora_relocation_relationship():
    #create a rescue zone
    response = client.post(
        "/api/rescue_flora/rescue_zone/", json={
            "name": "test_rescue_zone_102",
            "description": "test_description",
            "longitude": -65.000,
            "latitude": -17.000,
        },
    )
    assert response.status_code == 201, response.text
    data = response.json()
    rescue_zone_id = data["id"]

    #create a flora relocation 1
    response = client.post(
        "/api/rescue_flora/flora_relocation", json={
            "relocation_date": "2021-12-10T00:00:00",
            "size": 1.0,
            "epiphyte_phenology": "test_epiphyte_phenology140",
            "johanson_zone": "test_johanson_zone140",
            "relocation_position_latitude": -17.000,
            "relocation_position_longitude":-65.000,
            "bryophyte_number": 140,
            "dap_bryophyte": 140.0,
            "height_bryophyte": 140.0,
            "bryophyte_position": 140,
            "bark_type": "test_bark_type140",
            "infested_lianas": "Poco",
            "relocation_number": 140,
            "other_observations": "test_other_observations140",
            "rescue_zone_id": rescue_zone_id,
            "flora_rescue_id": 140,
            "specie_bryophyte_id": 140,
            "relocation_zone_id": 140,
        },
    )

    #create a flora relocation 2
    response = client.post(
        "/api/rescue_flora/flora_relocation", json={
            "relocation_date": "2021-12-10T00:00:00",
            "size": 2.0,
            "epiphyte_phenology": "test_epiphyte_phenology150",
            "johanson_zone": "test_johanson_zone150",
            "relocation_position_latitude": -17.000,
            "relocation_position_longitude":-65.000 ,
            "bryophyte_number": 150,
            "dap_bryophyte": 150.0,
            "height_bryophyte": 150.0,
            "bryophyte_position": 150,
            "bark_type": "test_bark_type150",
            "infested_lianas": "Poco",
            "relocation_number": 150,
            "other_observations": "test_other_observations150",
            "rescue_zone_id": rescue_zone_id,
            "flora_rescue_id": 150,
            "specie_bryophyte_id": 150,
            "relocation_zone_id": 150,
        },
    )


    #Make a query to data base to get flora_relocation with the same rescue_zone_id
    flora_relocation = db.query(FloraRelocation).filter(FloraRelocation.rescue_zone_id == rescue_zone_id).all()

    #Create a list of dictionaries with data
    flora_relocation_data = [
        {
            "relocation_date": s.relocation_date,
            "size": s.size,
            "epiphyte_phenology": s.epiphyte_phenology,
            "johanson_zone": s.johanson_zone,
            "relocation_position_latitude": s.relocation_position_latitude,
            "relocation_position_longitude": s.relocation_position_longitude,
            "bryophyte_number": s.bryophyte_number,
            "dap_bryophyte": s.dap_bryophyte,
            "height_bryophyte": s.height_bryophyte,
            "bryophyte_position": s.bryophyte_position,
            "bark_type": s.bark_type,
            "infested_lianas": s.infested_lianas,
            "relocation_number": s.relocation_number,
            "other_observations": s.other_observations,
            "rescue_zone_id": s.rescue_zone_id,
            "flora_rescue_id": s.flora_rescue_id,
            "specie_bryophyte_id": s.specie_bryophyte_id,
            "relocation_zone_id": s.relocation_zone_id,
        }
        for s in flora_relocation
    ]

    except_data = [
        {
            "relocation_date": datetime(2021, 12, 10, 0, 0),
            "size": 1.0,
            "epiphyte_phenology": "test_epiphyte_phenology140",
            "johanson_zone": "test_johanson_zone140",
            "relocation_position_latitude": -17.000,
            "relocation_position_longitude":-65.000 ,
            "bryophyte_number": 140,
            "dap_bryophyte": 140.0,
            "height_bryophyte": 140.0,
            "bryophyte_position": 140,
            "bark_type": "test_bark_type140",
            "infested_lianas": "Poco",
            "relocation_number": 140,
            "other_observations": "test_other_observations140",
            "rescue_zone_id": rescue_zone_id,
            "flora_rescue_id": 140,
            "specie_bryophyte_id": 140,
            "relocation_zone_id": 140,
        },
        {
            "relocation_date": datetime(2021, 12, 10, 0, 0),
            "size": 2.0,
            "epiphyte_phenology": "test_epiphyte_phenology150",
            "johanson_zone": "test_johanson_zone150",
            "relocation_position_latitude": -17.000,
            "relocation_position_longitude":-65.000 ,
            "bryophyte_number": 150,
            "dap_bryophyte": 150.0,
            "height_bryophyte": 150.0,
            "bryophyte_position": 150,
            "bark_type": "test_bark_type150",
            "infested_lianas": "Poco",
            "relocation_number": 150,
            "other_observations": "test_other_observations150",
            "rescue_zone_id": rescue_zone_id,
            "flora_rescue_id": 150,
            "specie_bryophyte_id": 150,
            "relocation_zone_id": 150,
        },
    ]

    #Compare if the data in the database is the same that the data inserted
    assert flora_relocation_data == except_data


#test for relationship between flora_rescue_zone adn plant_nursery
def test_relationship_flora_rescue_zone_plant_nursery():
    #create flora_rescolation_zone
    response = client.post(
        "/api/rescue_flora/relocation_zone/", json={
            "name": "test_relocation_zone_100",
        },
    )
    assert response.status_code == 201, response.text
    data = response.json()
    relocation_zone_id = data["id"]

    #create plant_nursery 1
    response = client.post(
        "/api/rescue_flora/plant_nursery", json={
            "entry_date": "2021-12-10T00:00:00",
            "cod_reg": "105",
            "health_status_epiphyte": "test_health_status_epiphyte10",
            "flowering_date": "2021-12-10T00:00:00",
            "vegetative_state": "test_vegetative_state10",
            "treatment_product": "test_treatment_product10",
            "is_pruned": False,
            "is_phytosanitary_treatment": False,
            "substrate": "test_substrate12",
            "departure_date": "2021-12-10T00:00:00",
            "rescue_zone_id": 12,
            "flora_rescue_id": 12,
            "specie_id": 12,
            "relocation_zone_id": relocation_zone_id,
        },
    )
    assert response.status_code == 201, response.text

    #create plant_nursery 2
    response = client.post(
        "/api/rescue_flora/plant_nursery", json={
            "entry_date": "2021-12-10T00:00:00",
            "cod_reg": "106",
            "health_status_epiphyte": "test_health_status_epiphyte20",
            "flowering_date": "2021-12-10T00:00:00",
            "vegetative_state": "test_vegetative_state20",
            "treatment_product": "test_treatment_product20",
            "is_pruned": False,
            "is_phytosanitary_treatment": False,
            "substrate": "test_substrate22",
            "departure_date": "2021-12-10T00:00:00",
            "rescue_zone_id": 22,
            "flora_rescue_id": 22,
            "specie_id": 22,
            "relocation_zone_id": relocation_zone_id,
        },
    )
    assert response.status_code == 201, response.text

    #Make a query to data base to get plant_nursery with the same relocation_zone_id
    plant_nursery = db.query(PlantNursery).filter(
        PlantNursery.relocation_zone_id == relocation_zone_id).all()

    #Create a list of dictionaries with data
    plant_nursery_data = [
        {
            "entry_date": p.entry_date,
            "cod_reg": p.cod_reg,
            "health_status_epiphyte": p.health_status_epiphyte,
            "flowering_date": p.flowering_date,
            "vegetative_state": p.vegetative_state,
            "treatment_product": p.treatment_product,
            "is_pruned": p.is_pruned,
            "is_phytosanitary_treatment": p.is_phytosanitary_treatment,
            "substrate": p.substrate,
            "departure_date": p.departure_date,
            "rescue_zone_id": p.rescue_zone_id,
            "flora_rescue_id": p.flora_rescue_id,
            "specie_id": p.specie_id,
            "relocation_zone_id": p.relocation_zone_id,
        }
        for p in plant_nursery
    ]

    except_data = [
        {
            "entry_date": datetime(2021, 12, 10, 0, 0),
            "cod_reg": "105",
            "health_status_epiphyte": "test_health_status_epiphyte10",
            "flowering_date": datetime(2021, 12, 10, 0, 0),
            "vegetative_state": "test_vegetative_state10",
            "treatment_product": "test_treatment_product10",
            "is_pruned": False,
            "is_phytosanitary_treatment": False,
            "substrate": "test_substrate12",
            "departure_date": datetime(2021, 12, 10, 0, 0),
            "rescue_zone_id": 12,
            "flora_rescue_id": 12,
            "specie_id": 12,
            "relocation_zone_id": relocation_zone_id,
        },
        {
            "entry_date": datetime(2021, 12, 10, 0, 0),
            "cod_reg": "106",
            "health_status_epiphyte": "test_health_status_epiphyte20",
            "flowering_date": datetime(2021, 12, 10, 0, 0),
            "vegetative_state": "test_vegetative_state20",
            "treatment_product": "test_treatment_product20",
            "is_pruned": False,
            "is_phytosanitary_treatment": False,
            "substrate": "test_substrate22",
            "departure_date": datetime(2021, 12, 10, 0, 0),
            "rescue_zone_id": 22,
            "flora_rescue_id": 22,
            "specie_id": 22,
            "relocation_zone_id": relocation_zone_id,
        },
    ]

    assert plant_nursery_data == except_data




