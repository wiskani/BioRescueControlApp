from httpx import Response, AsyncClient
from typing import Dict, Any, Union
import pytest

from app.tests.conftest import *
from app.tests.utils.species_example import *
from app.tests.utils.towers_example import *
from app.tests.conftest import async_client

"""
TEST CRUD HABITAT
"""
#test create habitat
@pytest.mark.asyncio
async def test_create_habitat(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_habitat = random_string()

    response = await async_client.post(
        "api/habitat", json={
            "name": name_habitat
        },
    )
    data = response.json()
    assert response.status_code == 201
    assert data["name"] == name_habitat
    assert "id" in data

#test create habitat with name already exists
@pytest.mark.asyncio
async def test_create_habitat_name_already_exists(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_habitat = random_string()

    response = await async_client.post(
        "api/habitat", json={
            "name": name_habitat
        },
    )
    data = response.json()
    assert response.status_code == 201

    response = await async_client.post(
        "api/habitat", json={
            "name": name_habitat
        },
    )
    data = response.json()
    print(f"La respuesta es: {data}")
    assert response.status_code == 409
    assert data["detail"] == "Habitat already exists"

#test get all habitats
@pytest.mark.asyncio
async def test_get_all_habitats(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    #create two habitats
    name_habitat1 = random_string()
    name_habitat2 = random_string()

    response = await async_client.post(
        "api/habitat", json={
            "name": name_habitat1
        },
    )
    assert response.status_code == 201

    response = await async_client.post(
        "api/habitat", json={
            "name": name_habitat2
        },
    )
    assert response.status_code == 201

    #get all habitats
    response = await async_client.get(
        "api/habitat",
    )
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2

#test get habitat by id
@pytest.mark.asyncio
async def test_get_habitat_by_id(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    #create habitat
    name_habitat = random_string()

    response = await async_client.post(
        "api/habitat", json={
            "name": name_habitat
        },
    )
    data = response.json()
    assert response.status_code == 201

    #get habitat by id
    response = await async_client.get(
        f"api/habitat/{data['id']}",
    )
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == name_habitat

#test get habitat by id not found
@pytest.mark.asyncio
async def test_get_habitat_by_id_not_found(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    #get habitat by id
    response = await async_client.get(
        f"api/habitat/1",
    )
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Habitat not found"

#test update habitat
@pytest.mark.asyncio
async def test_update_habitat(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    #create habitat
    name_habitat = random_string()

    response = await async_client.post(
        "api/habitat", json={
            "name": name_habitat
        },
    )
    data = response.json()
    assert response.status_code == 201

    #update habitat
    name_habitat2 = random_string()
    response = await async_client.put(
        f"api/habitat/{data['id']}", json={
            "name": name_habitat2
        },
    )
    data = response.json()
    print(f"La respuesta es: {data}")
    assert response.status_code == 200
    assert data["name"] == name_habitat2

#test update habitat not found
@pytest.mark.asyncio
async def test_update_habitat_not_found(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    #update habitat
    name_habitat2 = random_string()
    response = await async_client.put(
        f"api/habitat/1", json={
            "name": name_habitat2
        },
    )
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Habitat not found"

#test delete habitat
@pytest.mark.asyncio
async def test_delete_habitat(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    #create habitat
    name_habitat = random_string()

    response = await async_client.post(
        "api/habitat", json={
            "name": name_habitat
        },
    )
    data = response.json()
    assert response.status_code == 201

    #delete habitat
    response = await async_client.delete(
        f"api/habitat/{data['id']}",
    )
    data = response.json()
    print(f"La respuesta es: {data}")
    assert response.status_code == 200
    assert data["detail"] == "Habitat deleted successfully"

"""
TEST RESCUE MAMMALS
"""















