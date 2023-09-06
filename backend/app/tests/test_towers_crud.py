from pydantic import EmailStr
from requests import Response
from typing import Dict, Any, Union
from fastapi.testclient import TestClient

from app.tests.conftest import *
from app.tests.utils.towers_example import *
from app.crud.tower import get_clear_flora_id_by_tower_number

TOWER = create_random_tower()
TOWER_NUMBER = TOWER.number

db: Session = next(override_get_db())


"""
TEST FOR TOWERS CRUD
"""
#test for create a TOWER
def test_create_tower() -> None :
    response = client.post(
        "/api/towers", json={
            "number": 1,
            "latitude": 1.1,
            "longitude": 1.1,
        },
    )

    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    assert data["number"] == 1
    assert data["latitude"] == 1.1
    assert data["longitude"] == 1.1

#test create a tower with invalid number
def test_create_tower_invalid_number() -> None :

    response = client.post(
        "/api/towers", json={
            "number": 2,
            "latitude": 1.1,
            "longitude": 1.1,
        },
    )

    assert response.status_code == 201, response.text

    response = client.post(
        "/api/towers", json={
            "number": 2,
            "latitude": 1.1,
            "longitude": 1.1,
        },
    )

    assert response.status_code == 400, response.text
    #response text must to say Tower already registered
    assert response.text == '{"detail":"Tower already registered"}'

#test_update_tower
def test_update_tower() -> None :
    response = client.post(
        "/api/towers", json={
            "number": 3,
            "latitude": 1.1,
            "longitude": 1.1,
        },
    )

    assert response.status_code == 201, response.text

    data: Dict[str, Any] = response.json()

    response = client.put(
        f"/api/towers/{data['id']}", json={
            "number": 4,
            "latitude": 2.2,
            "longitude": 2.2,
        },
    )

    assert response.status_code == 200, response.text
    data: Dict[str, Any] = response.json()
    assert data["number"] == 4
    assert data["latitude"] == 2.2
    assert data["longitude"] == 2.2

#test for get all towers
def test_get_all_towers() -> None :
    #create 2 towers
    response = client.post(
        "/api/towers", json={
            "number": 5,
            "latitude": 1.1,
            "longitude": 1.1,
        },
    )

    assert response.status_code == 201, response.text

    response = client.post(
        "/api/towers", json={
            "number": 6,
            "latitude": 1.1,
            "longitude": 1.1,
        },
    )

    assert response.status_code == 201, response.text

    response = client.get(
        "/api/towers",
    )

    assert response.status_code == 200, response.text
    data: Dict[str, Any] = response.json()
    assert len(data) >= 1

"""
TEST FOR CRUD CLEAR FLORA
"""

#test for create a clear flora
def test_create_clear_flora() -> None :
    response = client.post(
        f"/api/clear_flora/{TOWER_NUMBER}", json={
            "is_clear": True,
            "clear_at": "2021-01-01T00:00:00",
        },
    )

    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    assert data["is_clear"] == True
    assert data["clear_at"] == "2021-01-01T00:00:00"

#test for create a clear flora with invalid tower number
def test_create_clear_flora_invalid_tower_number() -> None :
    #ceate a clear flora
    response = client.post(
        f"/api/clear_flora/{TOWER_NUMBER}", json={
            "is_clear": True,
            "clear_at": "2021-01-01T00:00:00",
        },
    )
    assert response.status_code == 404, response.text

#test for get all clear flora
def test_get_all_clear_flora() -> None :
    #get all clear flora
    response = client.get(
        "/api/clear_flora",
    )

    assert response.status_code == 200, response.text
    data: Dict[str, Any] = response.json()
    assert len(data) >= 1

#test for get a clear flora by tower number
def test_get_clear_flora_by_tower_number() -> None :
    #get clear flora by tower number
    response = client.get(
        f"/api/clear_flora/{TOWER_NUMBER}",
    )

    assert response.status_code == 200, response.text

#test for update a clear flora
def test_update_clear_flora() -> None :
    #get clear flora id
    response = client.put(
        f"/api/clear_flora/{TOWER_NUMBER}", json={
            "is_clear": False,
            "clear_at": "2021-01-01T00:00:00",
        },
    )

    assert response.status_code == 200, response.text
    data: Dict[str, Any] = response.json()
    assert data["is_clear"] == False
    assert data["clear_at"] == "2021-01-01T00:00:00"

#test for delete a clear flora
def test_delete_clear_flora() -> None :
    #delete clear flora
    response = client.delete(
        f"/api/clear_flora/{TOWER_NUMBER}",
    )
    #assert response message must say: Clear flora deleted successfully
    assert response.text == '{"message":"Clear flora deleted successfully"}'

"""
TEST FOR CRUD HERPETOFAUNA
"""

#test for create a herpetofauna
def test_create_herpetofauna() -> None :
    response = client.post(
        f"/api/clear_herpetofauna/{TOWER_NUMBER}", json={
            "is_clear": True,
            "clear_at": "2021-01-01T00:00:00",
        },
    )

    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    assert data["is_clear"] == True
    assert data["clear_at"] == "2021-01-01T00:00:00"

#test for create a herpetofauna with invalid tower number
def test_create_herpetofauna_invalid_tower_number() -> None :
    #ceate a herpetofauna
    response = client.post(
        f"/api/clear_herpetofauna/{TOWER_NUMBER}", json={
            "is_clear": True,
            "clear_at": "2021-01-01T00:00:00",
        },
    )
    assert response.status_code == 404, response.text

#test for get all herpetofauna
def test_get_all_herpetofauna() -> None :
    #get all herpetofauna
    response = client.get(
        "/api/clear_herpetofauna",
    )

    assert response.status_code == 200, response.text
    data: Dict[str, Any] = response.json()
    assert len(data) >= 1



