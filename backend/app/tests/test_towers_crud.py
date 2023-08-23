from pydantic import EmailStr
from requests import Response
from typing import Dict, Any, Union
from fastapi.testclient import TestClient

from app.tests.conftest import *
from app.tests.utils.users import *


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

