from requests import Response
from typing import Dict, Any, Union
from fastapi.testclient import TestClient

from app.tests.conftest import *
from app.tests.utils.users import *
from app.tests.utils.species_example import *

#fuctions to create a longitude and latitude
def create_longitude() -> float:
    return random.uniform(-180, 180)

def create_latitude() -> float:
    return random.uniform(-90, 90)

"""
TEST FOR RESCUE FLORA ZONE ENDPOINTS
"""

#test create a rescue zone endpoint
def test_create_rescue_zone() -> None:
    # create zone rescue
    response = client.post(
        "/api/rescue_flora/rescue_zone/", json={
            "name": "test_rescue_zone",
            "description": "test_description",
            "longitude": create_longitude(),
            "latitude": create_latitude(),
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    assert "id" in data
    assert data["name"] == "test_rescue_zone"
    assert data["description"] == "test_description"
    assert data["longitude"] >= -180 and data["longitude"] <= 180
    assert data["latitude"] >= -90 and data["latitude"] <= 90

#test create a rescue zone that already exists
def test_create_rescue_zone_that_already_exists() -> None:
    # create zone rescue
    response = client.post(
        "/api/rescue_flora/rescue_zone/", json={
            "name": "test_rescue_zone2",
            "description": "test_description2",
            "longitude": create_longitude(),
            "latitude": create_latitude(),
        },
    )
    assert response.status_code == 201, response.text

    # create zone rescue that already exists
    response = client.post(
        "/api/rescue_flora/rescue_zone/", json={
            "name": "test_rescue_zone2",
            "description": "test_description",
            "longitude": create_longitude(),
            "latitude": create_latitude(),
        },
    )
    assert response.status_code == 400, response.text

#test get all rescue zones
def test_get_all_rescue_zones() -> None:
    # create zone rescue
    response = client.post(
        "/api/rescue_flora/rescue_zone/", json={
            "name": "test_rescue_zone3",
            "description": "test_description3",
            "longitude": create_longitude(),
            "latitude": create_latitude(),
        },
    )
    assert response.status_code == 201, response.text

    # create zone rescue
    response = client.post(
        "/api/rescue_flora/rescue_zone/", json={
            "name": "test_rescue_zone4",
            "description": "test_description4",
            "longitude": create_longitude(),
            "latitude": create_latitude(),
        },
    )
    assert response.status_code == 201, response.text

    # get all rescue zones
    response = client.get("/api/rescue_flora/rescue_zone/")
    assert response.status_code == 200, response.text
    data: Dict[str, Any] = response.json()
    assert len(data) >= 2

#test get a rescue zone by id
def test_get_rescue_zone_by_id() -> None:
    # create zone rescue
    response = client.post(
        "/api/rescue_flora/rescue_zone/", json={
            "name": "test_rescue_zone5",
            "description": "test_description5",
            "longitude": create_longitude(),
            "latitude": create_latitude(),
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    rescue_zone_id: int = data["id"]

    # get a rescue zone by id
    response = client.get(f"/api/rescue_flora/rescue_zone/{rescue_zone_id}")
    assert response.status_code == 200, response.text
    data: Dict[str, Any] = response.json()
    assert data["name"] == "test_rescue_zone5"
    assert data["description"] == "test_description5"
    assert data["longitude"] >= -180 and data["longitude"] <= 180
    assert data["latitude"] >= -90 and data["latitude"] <= 90

#test get a rescue zone by id that does not exist
def test_get_rescue_zone_by_id_that_does_not_exist() -> None:
    # get a rescue zone by id that does not exist
    response = client.get("/api/rescue_flora/rescue_zone/999")
    assert response.status_code == 404, response.text

#test update a rescue zone by id
def test_update_rescue_zone_by_id() -> None:
    # create zone rescue
    response = client.post(
        "/api/rescue_flora/rescue_zone/", json={
            "name": "test_rescue_zone6",
            "description": "test_description6",
            "longitude": create_longitude(),
            "latitude": create_latitude(),
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    rescue_zone_id: int = data["id"]

    # update a rescue zone by id
    response = client.put(
        f"/api/rescue_flora/rescue_zone/{rescue_zone_id}", json={
            "name": "test_rescue_zone6",
            "description": "test_description6",
            "longitude": create_longitude(),
            "latitude": create_latitude(),
        },
    )
    assert response.status_code == 200, response.text
    data: Dict[str, Any] = response.json()
    assert data["name"] == "test_rescue_zone6"
    assert data["description"] == "test_description6"
    assert data["longitude"] >= -180 and data["longitude"] <= 180
    assert data["latitude"] >= -90 and data["latitude"] <= 90

#test delete a rescue zone by id
def test_delete_rescue_zone_by_id() -> None:
    # create zone rescue
    response = client.post(
        "/api/rescue_flora/rescue_zone/", json={
            "name": "test_rescue_zone7",
            "description": "test_description7",
            "longitude": create_longitude(),
            "latitude": create_latitude(),
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    rescue_zone_id: int = data["id"]

    # delete a rescue zone by id
    response = client.delete(f"/api/rescue_flora/rescue_zone/{rescue_zone_id}")
    assert response.status_code == 200, response.text

    # get a rescue zone by id that does not exist
    response = client.get(f"/api/rescue_flora/rescue_zone/{rescue_zone_id}")
    assert response.status_code == 404, response.text

"""
TEST FOR RELOCATION ZONE ENDPOINTS
"""

#test create a relocartion  zone 
def test_create_relocation_zone() -> None:
    # create zone relocation
    response = client.post(
        "/api/rescue_flora/relocation_zone/", json={
            "name": "test_relocation_zone",
        },
    )
    assert response.status_code == 201, response.text

#test create a relocation zone that already exists
def test_create_relocation_zone_that_already_exists() -> None:
    # create zone relocation
    response = client.post(
        "/api/rescue_flora/relocation_zone/", json={
            "name": "test_relocation_zone2",
        },
    )
    assert response.status_code == 201, response.text

    # create zone relocation that already exists
    response = client.post(
        "/api/rescue_flora/relocation_zone/", json={
            "name": "test_relocation_zone2",
        },
    )
    assert response.status_code == 400, response.text

#test get all relocation zones
def test_get_all_relocation_zones() -> None:
    # create zone relocation
    response = client.post(
        "/api/rescue_flora/relocation_zone/", json={
            "name": "test_relocation_zone3",
        },
    )
    assert response.status_code == 201, response.text

    # create zone relocation
    response = client.post(
        "/api/rescue_flora/relocation_zone/", json={
            "name": "test_relocation_zone4",
        },
    )
    assert response.status_code == 201, response.text

    # get all relocation zones
    response = client.get("/api/rescue_flora/relocation_zone/")
    assert response.status_code == 200, response.text
    data: Dict[str, Any] = response.json()
    assert len(data) >= 2
    
#test get a relocation zone by id
def test_get_relocation_zone_by_id() -> None:
    # create zone relocation
    response = client.post(
        "/api/rescue_flora/relocation_zone/", json={
            "name": "test_relocation_zone5",
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    relocation_zone_id: int = data["id"]

    # get a relocation zone by id
    response = client.get(f"/api/rescue_flora/relocation_zone/{relocation_zone_id}")
    assert response.status_code == 200, response.text
    data: Dict[str, Any] = response.json()
    assert data["name"] == "test_relocation_zone5"

#test get a relocation zone by id that does not exist
def test_get_relocation_zone_by_id_that_does_not_exist() -> None:
    # get a relocation zone by id that does not exist
    response = client.get("/api/rescue_flora/relocation_zone/999")
    assert response.status_code == 404, response.text

#test update a relocation zone by id
def test_update_relocation_zone_by_id() -> None:
    # create zone relocation
    response = client.post(
        "/api/rescue_flora/relocation_zone/", json={
            "name": "test_relocation_zone6",
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    relocation_zone_id: int = data["id"]

    # update a relocation zone by id
    response = client.put(
        f"/api/rescue_flora/relocation_zone/{relocation_zone_id}", json={
            "name": "test_relocation_zone6",
        },
    )
    assert response.status_code == 200, response.text
    data: Dict[str, Any] = response.json()
    assert data["name"] == "test_relocation_zone6"

#test delete a relocation zone by id
def test_delete_relocation_zone_by_id() -> None:
    # create zone relocation
    response = client.post(
        "/api/rescue_flora/relocation_zone/", json={
            "name": "test_relocation_zone7",
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    relocation_zone_id: int = data["id"]

    # delete a relocation zone by id
    response = client.delete(f"/api/rescue_flora/relocation_zone/{relocation_zone_id}")
    assert response.status_code == 200, response.text

    # get a relocation zone by id that does not exist
    response = client.get(f"/api/rescue_flora/relocation_zone/{relocation_zone_id}")
    assert response.status_code == 404, response.text

"""
TEST FOR FLORA RESCUE ENDPOINTS
"""

#test create a flora rescue
def test_create_flora_rescue() -> None:
    # create flora rescue
    response = client.post(
        "/api/rescue_flora", json={
            "epiphyte_number": 1,
            "rescue_date": "2021-10-10T00:00:00",
            "rescue_area_latitude": create_latitude(),
            "rescue_area_longitude": create_longitude(),
            "dap_bryophyte": 1.0,
            "height_bryophyte": 1.0,
            "bryophyte_position": 1,
            "growth_habit": "test_growth_habit",
            "epiphyte_phenology": "test_epiphyte_phenology",
            "health_status_epiphyte": "test_health_status_epiphyte",
            "other_observations": "test_other_observations",
            "specie_bryophyte_id": 1,
            "specie_epiphyte_id": 1,
            "rescue_zone_id": 1,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    assert "id" in data
    assert data["epiphyte_number"] == 1
    assert data["rescue_date"] == "2021-10-10T00:00:00"
    assert data["rescue_area_latitude"] >= -90 and data["rescue_area_latitude"] <= 90
    assert data["rescue_area_longitude"] >= -180 and data["rescue_area_longitude"] <= 180
    assert data["dap_bryophyte"] == 1.0
    assert data["height_bryophyte"] == 1.0
    assert data["bryophyte_position"] == 1
    assert data["growth_habit"] == "test_growth_habit"
    assert data["epiphyte_phenology"] == "test_epiphyte_phenology"
    assert data["health_status_epiphyte"] == "test_health_status_epiphyte"
    assert data["other_observations"] == "test_other_observations"
    assert data["specie_bryophyte_id"] == 1
    assert data["specie_epiphyte_id"] == 1
    assert data["rescue_zone_id"] == 1

#test create a flora rescue that already exists
def test_create_flora_rescue_that_already_exists() -> None:
    # create flora rescue
    response = client.post(
        "/api/rescue_flora", json={
            "epiphyte_number": 2,
            "rescue_date": "2021-12-10T00:00:00",
            "rescue_area_latitude": create_latitude(),
            "rescue_area_longitude": create_longitude(),
            "dap_bryophyte": 2.0,
            "height_bryophyte": 2.0,
            "bryophyte_position": 2,
            "growth_habit": "test_growth_habit2",
            "epiphyte_phenology": "test_epiphyte_phenology2",
            "health_status_epiphyte": "test_health_status_epiphyte2",
            "other_observations": "test_other_observations2",
            "specie_bryophyte_id": 2,
            "specie_epiphyte_id": 2,
            "rescue_zone_id": 2,
        },
    )
    assert response.status_code == 201, response.text

    # create flora rescue that already exists
    response = client.post(
        "/api/rescue_flora", json={
            "epiphyte_number": 2,
            "rescue_date": "2021-12-10T00:00:00",
            "rescue_area_latitude": create_latitude(),
            "rescue_area_longitude": create_longitude(),
            "dap_bryophyte": 2.0,
            "height_bryophyte": 2.0,
            "bryophyte_position": 2,
            "growth_habit": "test_growth_habit2",
            "epiphyte_phenology": "test_epiphyte_phenology2",
            "health_status_epiphyte": "test_health_status_epiphyte2",
            "other_observations": "test_other_observations2",
            "specie_bryophyte_id": 2,
            "specie_epiphyte_id": 2,
            "rescue_zone_id": 2,
        },
    )
    assert response.status_code == 400, response.text

#test get all flora rescues
def test_read_all_flora_rescues() -> None:
    # create flora rescue
    response = client.post(
        "/api/rescue_flora", json={
            "epiphyte_number": 3,
            "rescue_date": "2021-12-10T00:00:00",
            "rescue_area_latitude": create_latitude(),
            "rescue_area_longitude": create_longitude(),
            "dap_bryophyte": 3.0,
            "height_bryophyte": 3.0,
            "bryophyte_position": 3,
            "growth_habit": "test_growth_habit3",
            "epiphyte_phenology": "test_epiphyte_phenology3",
            "health_status_epiphyte": "test_health_status_epiphyte3",
            "other_observations": "test_other_observations3",
            "specie_bryophyte_id": 3,
            "specie_epiphyte_id": 3,
            "rescue_zone_id": 3,
        },
    )
    assert response.status_code == 201, response.text

    # create flora rescue
    response = client.post(
        "/api/rescue_flora", json={
            "epiphyte_number": 4,
            "rescue_date": "2021-12-10T00:00:00",
            "rescue_area_latitude": create_latitude(),
            "rescue_area_longitude": create_longitude(),
            "dap_bryophyte": 4.0,
            "height_bryophyte": 4.0,
            "bryophyte_position": 4,
            "growth_habit": "test_growth_habit4",
            "epiphyte_phenology": "test_epiphyte_phenology4",
            "health_status_epiphyte": "test_health_status_epiphyte4",
            "other_observations": "test_other_observations4",
            "specie_bryophyte_id": 4,
            "specie_epiphyte_id": 4,
            "rescue_zone_id": 4,
        },
    )
    assert response.status_code == 201, response.text

    # get all flora rescues
    response = client.get("/api/rescue_flora")
    assert response.status_code == 200, response.text
    data: List[Dict[str, Any]] = response.json()
    assert len(data) >= 2

#test get a flora rescue by id
def test_read_flora_rescue_by_id() -> None:
    # create flora rescue
    response = client.post(
        "/api/rescue_flora", json={
            "epiphyte_number": 5,
            "rescue_date": "2021-12-10T00:00:00",
            "rescue_area_latitude": create_latitude(),
            "rescue_area_longitude": create_longitude(),
            "dap_bryophyte": 5.0,
            "height_bryophyte": 5.0,
            "bryophyte_position": 5,
            "growth_habit": "test_growth_habit5",
            "epiphyte_phenology": "test_epiphyte_phenology5",
            "health_status_epiphyte": "test_health_status_epiphyte5",
            "other_observations": "test_other_observations5",
            "specie_bryophyte_id": 5,
            "specie_epiphyte_id": 5,
            "rescue_zone_id": 5,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()

    # get a flora rescue by id
    response = client.get(f"/api/rescue_flora/{data['id']}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert "id" in data
    assert data["epiphyte_number"] == 5
    assert data["rescue_date"] == "2021-12-10T00:00:00"
    assert data["rescue_area_latitude"] >= -90 and data["rescue_area_latitude"] <= 90
    assert data["rescue_area_longitude"] >= -180 and data["rescue_area_longitude"] <= 180
    assert data["dap_bryophyte"] == 5.0
    assert data["height_bryophyte"] == 5.0
    assert data["bryophyte_position"] == 5
    assert data["growth_habit"] == "test_growth_habit5"
    assert data["epiphyte_phenology"] == "test_epiphyte_phenology5"
    assert data["health_status_epiphyte"] == "test_health_status_epiphyte5"
    assert data["other_observations"] == "test_other_observations5"
    assert data["specie_bryophyte_id"] == 5
    assert data["specie_epiphyte_id"] == 5
    assert data["rescue_zone_id"] == 5

#test get a flora rescue by id not found
def test_read_flora_rescue_by_id_not_found() -> None:
    # get a flora rescue by id not found
    response = client.get("/api/rescue_flora/0")
    assert response.status_code == 404, response.text
    
#test update a flora rescue
def test_update_flora_rescue() -> None:
    # create flora rescue
    response = client.post(
        "/api/rescue_flora", json={
            "epiphyte_number": 6,
            "rescue_date": "2021-12-10T00:00:00",
            "rescue_area_latitude": create_latitude(),
            "rescue_area_longitude": create_longitude(),
            "dap_bryophyte": 6.0,
            "height_bryophyte": 6.0,
            "bryophyte_position": 6,
            "growth_habit": "test_growth_habit6",
            "epiphyte_phenology": "test_epiphyte_phenology6",
            "health_status_epiphyte": "test_health_status_epiphyte6",
            "other_observations": "test_other_observations6",
            "specie_bryophyte_id": 6,
            "specie_epiphyte_id": 6,
            "rescue_zone_id": 6,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    id = data["id"]

    # update a flora rescue
    response = client.put(
       f"/api/rescue_flora/{id}", json={
            "epiphyte_number": 7,
            "rescue_date": "2021-12-11T00:00:00",
            "rescue_area_latitude": create_latitude(),
            "rescue_area_longitude": create_longitude(),
            "dap_bryophyte": 7.0,
            "height_bryophyte": 7.0,
            "bryophyte_position": 7,
            "growth_habit": "test_growth_habit7",
            "epiphyte_phenology": "test_epiphyte_phenology7",
            "health_status_epiphyte": "test_health_status_epiphyte7",
            "other_observations": "test_other_observations7",
            "specie_bryophyte_id": 7,
            "specie_epiphyte_id": 7,
            "rescue_zone_id": 7,
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "id" in data
    assert data["epiphyte_number"] == 7
    assert data["rescue_date"] == "2021-12-11T00:00:00"
    assert data["rescue_area_latitude"] >= -90 and data["rescue_area_latitude"] <= 90
    assert data["rescue_area_longitude"] >= -180 and data["rescue_area_longitude"] <= 180
    assert data["dap_bryophyte"] == 7.0
    assert data["height_bryophyte"] == 7.0
    assert data["bryophyte_position"] == 7
    assert data["growth_habit"] == "test_growth_habit7"
    assert data["epiphyte_phenology"] == "test_epiphyte_phenology7"
    assert data["health_status_epiphyte"] == "test_health_status_epiphyte7"
    assert data["other_observations"] == "test_other_observations7"
    assert data["specie_bryophyte_id"] == 7
    assert data["specie_epiphyte_id"] == 7
    assert data["rescue_zone_id"] == 7

#test update a flora rescue not found
def test_update_flora_rescue_not_found() -> None:
    # update a flora rescue not found
    response = client.put(
        "/api/rescue_flora/0", json={
            "epiphyte_number": 8,
            "rescue_date": "2021-12-10T00:00:00",
            "rescue_area_latitude": create_latitude(),
            "rescue_area_longitude": create_longitude(),
            "dap_bryophyte": 8.0,
            "height_bryophyte": 8.0,
            "bryophyte_position": 8,
            "growth_habit": "test_growth_habit8",
            "epiphyte_phenology": "test_epiphyte_phenology8",
            "health_status_epiphyte": "test_health_status_epiphyte8",
            "other_observations": "test_other_observations8",
            "specie_bryophyte_id": 8,
            "specie_epiphyte_id": 8,
            "rescue_zone_id": 8,
        },
    )
    assert response.status_code == 404, response.text

#test delete a flora rescue
def test_delete_flora_rescue() -> None:
    # create flora rescue
    response = client.post(
        "/api/rescue_flora", json={
            "epiphyte_number": 9,
            "rescue_date": "2021-12-10T00:00:00",
            "rescue_area_latitude": create_latitude(),
            "rescue_area_longitude": create_longitude(),
            "dap_bryophyte": 9.0,
            "height_bryophyte": 9.0,
            "bryophyte_position": 9,
            "growth_habit": "test_growth_habit9",
            "epiphyte_phenology": "test_epiphyte_phenology9",
            "health_status_epiphyte": "test_health_status_epiphyte9",
            "other_observations": "test_other_observations9",
            "specie_bryophyte_id": 9,
            "specie_epiphyte_id": 9,
            "rescue_zone_id": 9,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()

    # delete a flora rescue
    response = client.delete(f"/api/rescue_flora/{data['id']}")
    assert response.status_code == 200, response.text

#test delete a flora rescue not found
def test_delete_flora_rescue_not_found() -> None:
    # delete a flora rescue not found
    response = client.delete("/api/rescue_flora/0")
    assert response.status_code == 404, response.text

"""
TESTS FOR PLANT NURSERY
"""

#test create a plant nursery
def test_create_plant_nursery() -> None:
    #fuction to create a randon numnert int in a range of 111 to 999

    # create plant nursery
    response = client.post(
        "/api/rescue_flora/plant_nursery", json={
            "entry_date": "2021-12-10T00:00:00",
            "cod_reg": 10,
            "health_status_epiphyte": "test_health_status_epiphyte10",
            "flowering_date": "2021-12-10T00:00:00",
            "treatment_product": "test_treatment_product10",
            "is_phytosanitary_treatment": False,
            "substrate": "test_substrate10",
            "departure_date": "2021-12-10T00:00:00",
            "rescue_zone_id": 10,
            "flora_rescue_id": 10,
            "specie_id": 10,
            "relocation_zone_id": 10,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    assert "id" in data
    assert data["entry_date"] == "2021-12-10T00:00:00"
    assert data["cod_reg"] == 10
    assert data["health_status_epiphyte"] == "test_health_status_epiphyte10"
    assert data["flowering_date"] == "2021-12-10T00:00:00"
    assert data["treatment_product"] == "test_treatment_product10"
    assert data["is_phytosanitary_treatment"] == False
    assert data["substrate"] == "test_substrate10"
    assert data["departure_date"] == "2021-12-10T00:00:00"
    assert data["rescue_zone_id"] == 10
    assert data["flora_rescue_id"] == 10
    assert data["specie_id"] == 10
    assert data["relocation_zone_id"] == 10

#test create a plant nursery that already exists
def test_create_plant_nursery_already_exists() -> None:
    # create plant nursery that already exists
    response = client.post(
        "/api/rescue_flora/plant_nursery", json={
            "entry_date": "2021-12-10T00:00:00",
            "cod_reg": 10,
            "health_status_epiphyte": "test_health_status_epiphyte10",
            "flowering_date": "2021-12-10T00:00:00",
            "treatment_product": "test_treatment_product10",
            "is_phytosanitary_treatment": False,
            "substrate": "test_substrate10",
            "departure_date": "2021-12-10T00:00:00",
            "rescue_zone_id": 10,
            "flora_rescue_id": 10,
            "specie_id": 10,
            "relocation_zone_id": 10,
        },
    )
    assert response.status_code == 400, response.text

#test get all plant nursery
def test_read_all_plant_nursery() -> None:
    # create two plant nursery
    response = client.post(
        "/api/rescue_flora/plant_nursery", json={
            "entry_date": "2021-12-10T00:00:00",
            "cod_reg": 11,
            "health_status_epiphyte": "test_health_status_epiphyte11",
            "flowering_date": "2021-12-10T00:00:00",
            "treatment_product": "test_treatment_product11",
            "is_phytosanitary_treatment": False,
            "substrate": "test_substrate11",
            "departure_date": "2021-12-10T00:00:00",
            "rescue_zone_id": 11,
            "flora_rescue_id": 11,
            "specie_id": 11,
            "relocation_zone_id": 11,
        },
    )
    assert response.status_code == 201, response.text
    response = client.post(
        "/api/rescue_flora/plant_nursery", json={
            "entry_date": "2021-12-10T00:00:00",
            "cod_reg": 12,
            "health_status_epiphyte": "test_health_status_epiphyte12",
            "flowering_date": "2021-12-10T00:00:00",
            "treatment_product": "test_treatment_product12",
            "is_phytosanitary_treatment": False,
            "substrate": "test_substrate12",
            "departure_date": "2021-12-10T00:00:00",
            "rescue_zone_id": 12,
            "flora_rescue_id": 12,
            "specie_id": 12,
            "relocation_zone_id": 12,
        },
    )
    assert response.status_code == 201, response.text

    # read all plant nursery
    response = client.get("/api/plant_nurseries")
    assert response.status_code == 200, response.text
    data: List[Dict[str, Any]] = response.json()
    assert len(data) >= 2

#test get a plant nursery by id
def test_read_plant_nursery() -> None:
    # create a plant nursery
    response = client.post(
        "/api/rescue_flora/plant_nursery", json={
            "entry_date": "2021-12-10T00:00:00",
            "cod_reg": 13,
            "health_status_epiphyte": "test_health_status_epiphyte13",
            "flowering_date": "2021-12-10T00:00:00",
            "treatment_product": "test_treatment_product13",
            "is_phytosanitary_treatment": False,
            "substrate": "test_substrate13",
            "departure_date": "2021-12-10T00:00:00",
            "rescue_zone_id": 13,
            "flora_rescue_id": 13,
            "specie_id": 13,
            "relocation_zone_id": 13,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    # read a plant nursery by id
    response = client.get(f"/api/rescue_flora/plant_nursery/{data['id']}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["entry_date"] == "2021-12-10T00:00:00"
    assert data["cod_reg"] == 13
    assert data["health_status_epiphyte"] == "test_health_status_epiphyte13"
    assert data["flowering_date"] == "2021-12-10T00:00:00"
    assert data["treatment_product"] == "test_treatment_product13"
    assert data["is_phytosanitary_treatment"] == False
    assert data["substrate"] == "test_substrate13"
    assert data["departure_date"] == "2021-12-10T00:00:00"
    assert data["rescue_zone_id"] == 13
    assert data["flora_rescue_id"] == 13
    assert data["specie_id"] == 13
    assert data["relocation_zone_id"] == 13

"""
TEST FOR RELOCATION FLORA 
"""
#test create a relocation flora
def test_create_relocation_flora() -> None:
    # create relocation flora
    response = client.post(
        "/api/rescue_flora/flora_relocation", json={
            "relocation_date": "2021-12-10T00:00:00",
            "size": 1.0,
            "epiphyte_phenology": "test_epiphyte_phenology14",
            "johanson_zone": "test_johanson_zone14",
            "relocation_position_latitude": create_latitude(),
            "relocation_position_longitude": create_longitude(),
            "bryophyte_number": 14,
            "dap_bryophyte": 14.0,
            "height_bryophyte": 14.0,
            "bryophyte_position": 14,
            "bark_type": "test_bark_type14",
            "is_infested_lianas": False,
            "relocation_number": 14,
            "other_observations": "test_other_observations14",
            "rescue_zone_id": 14,
            "flora_rescue_id": 14,
            "specie_bryophyte_id": 14,
            "relocation_zone_id": 14,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    assert "id" in data
    assert data["relocation_date"] == "2021-12-10T00:00:00"
    assert data["size"] == 1.0
    assert data["epiphyte_phenology"] == "test_epiphyte_phenology14"
    assert data["johanson_zone"] == "test_johanson_zone14"
    assert data["relocation_position_latitude"] >= -90 and data["relocation_position_latitude"] <= 90
    assert data["relocation_position_longitude"] >= -180 and data["relocation_position_longitude"] <= 180
    assert data["bryophyte_number"] == 14
    assert data["dap_bryophyte"] == 14.0
    assert data["height_bryophyte"] == 14.0
    assert data["bryophyte_position"] == 14
    assert data["bark_type"] == "test_bark_type14"
    assert data["is_infested_lianas"] == False
    assert data["relocation_number"] == 14
    assert data["other_observations"] == "test_other_observations14"
    assert data["rescue_zone_id"] == 14
    assert data["flora_rescue_id"] == 14
    assert data["specie_bryophyte_id"] == 14
    assert data["relocation_zone_id"] == 14

#test create a relocation flora that already exists
def test_create_relocation_flora_already_exists() -> None:
    # create relocation flora that already exists
    response = client.post(
        "/api/rescue_flora/flora_relocation", json={
            "relocation_date": "2021-12-10T00:00:00",
            "size": 1.0,
            "epiphyte_phenology": "test_epiphyte_phenology14",
            "johanson_zone": "test_johanson_zone14",
            "relocation_position_latitude": create_latitude(),
            "relocation_position_longitude": create_longitude(),
            "bryophyte_number": 14,
            "dap_bryophyte": 14.0,
            "height_bryophyte": 14.0,
            "bryophyte_position": 14,
            "bark_type": "test_bark_type14",
            "is_infested_lianas": False,
            "relocation_number": 14,
            "other_observations": "test_other_observations14",
            "rescue_zone_id": 14,
            "flora_rescue_id": 14,
            "specie_bryophyte_id": 14,
            "relocation_zone_id": 14,
        },
    )
    assert response.status_code == 400, response.text

#test get all relocation flora
def test_read_all_relocation_flora() -> None:
    # create two relocation flora
    response = client.post(
        "/api/rescue_flora/flora_relocation", json={
            "relocation_date": "2021-12-10T00:00:00",
            "size": 2.0,
            "epiphyte_phenology": "test_epiphyte_phenology15",
            "johanson_zone": "test_johanson_zone15",
            "relocation_position_latitude": create_latitude(),
            "relocation_position_longitude": create_longitude(),
            "bryophyte_number": 15,
            "dap_bryophyte": 15.0,
            "height_bryophyte": 15.0,
            "bryophyte_position": 15,
            "bark_type": "test_bark_type15",
            "is_infested_lianas": False,
            "relocation_number": 15,
            "other_observations": "test_other_observations15",
            "rescue_zone_id": 15,
            "flora_rescue_id": 15,
            "specie_bryophyte_id": 15,
            "relocation_zone_id": 15,
        },
    )
    assert response.status_code == 201, response.text
    response = client.post(
        "/api/rescue_flora/flora_relocation", json={
            "relocation_date": "2021-12-10T00:00:00",
            "size": 3.0,
            "epiphyte_phenology": "test_epiphyte_phenology16",
            "johanson_zone": "test_johanson_zone16",
            "relocation_position_latitude": create_latitude(),
            "relocation_position_longitude": create_longitude(),
            "bryophyte_number": 16,
            "dap_bryophyte": 16.0,
            "height_bryophyte": 16.0,
            "bryophyte_position": 16,
            "bark_type": "test_bark_type16",
            "is_infested_lianas": False,
            "relocation_number": 16,
            "other_observations": "test_other_observations16",
            "rescue_zone_id": 16,
            "flora_rescue_id": 16,
            "specie_bryophyte_id": 16,
            "relocation_zone_id": 16,
        },
    )
    assert response.status_code == 201, response.text
    # read all relocation flora
    response = client.get("/api/flora_relocations")
    assert response.status_code == 200, response.text
    data: List[Dict[str, Any]] = response.json()
    assert len(data) >= 2

#test get a relocation flora by id
def test_read_relocation_flora() -> None:
    #create a relocation flora
    response = client.post(
        "/api/rescue_flora/flora_relocation", json={
            "relocation_date": "2021-12-10T00:00:00",
            "size": 4.0,
            "epiphyte_phenology": "test_epiphyte_phenology17",
            "johanson_zone": "test_johanson_zone17",
            "relocation_position_latitude": create_latitude(),
            "relocation_position_longitude": create_longitude(),
            "bryophyte_number": 17,
            "dap_bryophyte": 17.0,
            "height_bryophyte": 17.0,
            "bryophyte_position": 17,
            "bark_type": "test_bark_type17",
            "is_infested_lianas": False,
            "relocation_number": 17,
            "other_observations": "test_other_observations17",
            "rescue_zone_id": 17,
            "flora_rescue_id": 17,
            "specie_bryophyte_id": 17,
            "relocation_zone_id": 17,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    id = data["id"]
    # read a relocation flora by id
    response = client.get(f"/api/rescue_flora/flora_relocation/{id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["relocation_date"] == "2021-12-10T00:00:00"
    assert data["size"] == 4.0
    assert data["epiphyte_phenology"] == "test_epiphyte_phenology17"
    assert data["johanson_zone"] == "test_johanson_zone17"
    assert data["relocation_position_latitude"] >= -90 and data["relocation_position_latitude"] <= 90
    assert data["relocation_position_longitude"] >= -180 and data["relocation_position_longitude"] <= 180
    assert data["bryophyte_number"] == 17
    assert data["dap_bryophyte"] == 17.0
    assert data["height_bryophyte"] == 17.0
    assert data["bryophyte_position"] == 17
    assert data["bark_type"] == "test_bark_type17"
    assert data["is_infested_lianas"] == False
    assert data["relocation_number"] == 17
    assert data["other_observations"] == "test_other_observations17"
    assert data["rescue_zone_id"] == 17
    assert data["flora_rescue_id"] == 17
    assert data["specie_bryophyte_id"] == 17
    assert data["relocation_zone_id"] == 17

#test update a relocation flora
def test_update_relocation_flora() -> None:
    #create a relocation flora
    response = client.post(
        "/api/rescue_flora/flora_relocation", json={
            "relocation_date": "2021-12-10T00:00:00",
            "size": 5.0,
            "epiphyte_phenology": "test_epiphyte_phenology18",
            "johanson_zone": "test_johanson_zone18",
            "relocation_position_latitude": create_latitude(),
            "relocation_position_longitude": create_longitude(),
            "bryophyte_number": 18,
            "dap_bryophyte": 18.0,
            "height_bryophyte": 18.0,
            "bryophyte_position": 18,
            "bark_type": "test_bark_type18",
            "is_infested_lianas": False,
            "relocation_number": 18,
            "other_observations": "test_other_observations18",
            "rescue_zone_id": 18,
            "flora_rescue_id": 18,
            "specie_bryophyte_id": 18,
            "relocation_zone_id": 18,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    id = data["id"]
    # update a relocation flora
    response = client.put(
        f"/api/rescue_flora/flora_relocation/{id}", json={
            "relocation_date": "2021-12-10T00:00:00",
            "size": 6.0,
            "epiphyte_phenology": "test_epiphyte_phenology19",
            "johanson_zone": "test_johanson_zone19",
            "relocation_position_latitude": create_latitude(),
            "relocation_position_longitude": create_longitude(),
            "bryophyte_number": 19,
            "dap_bryophyte": 19.0,
            "height_bryophyte": 19.0,
            "bryophyte_position": 19,
            "bark_type": "test_bark_type19",
            "is_infested_lianas": False,
            "relocation_number": 19,
            "other_observations": "test_other_observations19",
            "rescue_zone_id": 19,
            "flora_rescue_id": 19,
            "specie_bryophyte_id": 19,
            "relocation_zone_id": 19,
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["relocation_date"] == "2021-12-10T00:00:00"
    assert data["size"] == 6.0
    assert data["epiphyte_phenology"] == "test_epiphyte_phenology19"
    assert data["johanson_zone"] == "test_johanson_zone19"
    assert data["relocation_position_latitude"] >= -90 and data["relocation_position_latitude"] <= 90
    assert data["relocation_position_longitude"] >= -180 and data["relocation_position_longitude"] <= 180
    assert data["bryophyte_number"] == 19
    assert data["dap_bryophyte"] == 19.0
    assert data["height_bryophyte"] == 19.0
    assert data["bryophyte_position"] == 19
    assert data["bark_type"] == "test_bark_type19"
    assert data["is_infested_lianas"] == False
    assert data["relocation_number"] == 19
    assert data["other_observations"] == "test_other_observations19"
    assert data["rescue_zone_id"] == 19
    assert data["flora_rescue_id"] == 19
    assert data["specie_bryophyte_id"] == 19
    assert data["relocation_zone_id"] == 19

#test delete a relocation flora
def test_delete_relocation_flora() -> None:
    #create a relocation flora
    response = client.post(
        "/api/rescue_flora/flora_relocation", json={
            "relocation_date": "2021-12-10T00:00:00",
            "size": 7.0,
            "epiphyte_phenology": "test_epiphyte_phenology20",
            "johanson_zone": "test_johanson_zone20",
            "relocation_position_latitude": create_latitude(),
            "relocation_position_longitude": create_longitude(),
            "bryophyte_number": 20,
            "dap_bryophyte": 20.0,
            "height_bryophyte": 20.0,
            "bryophyte_position": 20,
            "bark_type": "test_bark_type20",
            "is_infested_lianas": False,
            "relocation_number": 20,
            "other_observations": "test_other_observations20",
            "rescue_zone_id": 20,
            "flora_rescue_id": 20,
            "specie_bryophyte_id": 20,
            "relocation_zone_id": 20,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    id = data["id"]
    # delete a relocation flora
    response = client.delete(f"/api/rescue_flora/flora_relocation/{id}")
    assert response.status_code == 200, response.text

    














