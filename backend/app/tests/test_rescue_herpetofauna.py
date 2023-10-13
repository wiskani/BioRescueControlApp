from httpx import Response, AsyncClient
from typing import Dict, Any, Union
import pytest

from app.tests.conftest import *
from app.tests.utils.users import *
from app.tests.utils.species_example import *
from app.tests.utils.towers_example import *
from app.tests.utils.rescue_herpetofauna import *
from app.tests.conftest import async_client

"""
TEST CRUD FOR AGE GROUP
"""
#test create age group
@pytest.mark.asyncio
async def test_create_age_group(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_age = random_string()

    response = await async_client.post(
        "/api/age_group", json={
            "name": name_age
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == name_age
    assert "id" in data

#test create age group with name already exists
@pytest.mark.asyncio
async def test_create_age_group_name_already_exists(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_age = random_string()

    response = await async_client.post(
        "/api/age_group", json={
            "name": name_age
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == name_age
    assert "id" in data

    response = await async_client.post(
        "/api/age_group", json={
            "name": name_age
        },
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Age group name already exists"

#test get all age groups
@pytest.mark.asyncio
async def test_get_all_age_groups(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_age = random_string()

    response = await async_client.post(
        "/api/age_group", json={
            "name": name_age
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == name_age
    assert "id" in data

    response = await async_client.get(
        "/api/age_group",
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

#test get age group by id
@pytest.mark.asyncio
async def test_get_age_group_by_id(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_age = random_string()

    response = await async_client.post(
        "/api/age_group", json={
            "name": name_age
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == name_age
    assert "id" in data

    response = await async_client.get(
        f"/api/age_group/{data['id']}",
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == name_age
    assert "id" in data

#test get age group by id not found
@pytest.mark.asyncio
async def test_get_age_group_by_id_not_found(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    response = await async_client.get(
        f"/api/age_group/999999999",
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Age group not found"

#test update age group by id
@pytest.mark.asyncio
async def test_update_age_group_by_id(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_age = random_string()
    new_name_age = random_string()

    response = await async_client.post(
        "/api/age_group", json={
            "name": name_age
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == name_age
    assert "id" in data

    response = await async_client.put(
        f"/api/age_group/{data['id']}", json={
            "name": new_name_age
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == new_name_age
    assert "id" in data

#test update age group by id not found
@pytest.mark.asyncio
async def test_update_age_group_by_id_not_found(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    response = await async_client.put(
        f"/api/age_group/999999999", json={
            "name": random_string()
        },
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Age group not found"

#test delete age group by id
@pytest.mark.asyncio
async def test_delete_age_group_by_id(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_age = random_string()

    response = await async_client.post(
        "/api/age_group", json={
            "name": name_age
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == name_age
    assert "id" in data

    response = await async_client.delete(
        f"/api/age_group/{data['id']}",
    )
    assert response.status_code == 200
    data = response.json()
    assert data["detail"] == "Age group deleted successfully"

"""
TEST CRUD FOR MARK HERPETOFAUNA
"""

#test create mark herpetofauna
@pytest.mark.asyncio
async def test_create_mark_herpetofauna(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    number_mark = random_string()
    tower_id =  await create_random_tower(async_client)
    species_id = await create_specie(async_client)
    age_group_id = await create_age_group(async_client)

    response = await async_client.post(
        "/api/mark_herpetofauna", json={
            "date": "2021-10-10",
            "number": number_mark,
            "code": "123456789",
            "gender": True,
            "LHC": 1.5,
            "weight": 1.5,
            "is_photo_mark": True,
            "is_elastomer_mark": True,
            "tower_id": tower_id
            "specie_id": species_id
            "age_group_id": age_group_id
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["number"] == number_mark
    assert "id" in data




