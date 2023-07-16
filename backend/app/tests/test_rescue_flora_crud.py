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
    print(id)

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





