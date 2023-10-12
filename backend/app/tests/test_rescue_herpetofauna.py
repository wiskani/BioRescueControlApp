from httpx import Response, AsyncClient
from typing import Dict, Any, Union
import pytest

from app.tests.conftest import *
from app.tests.utils.users import *
from app.tests.utils.species_example import *
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





