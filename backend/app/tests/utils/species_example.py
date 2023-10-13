import random
import string
import pytest
from httpx import Response, AsyncClient
from typing import Dict, Any
from app.tests.conftest import *

#make a fuction that return a random string of 10 characters
def random_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=10))



#make a fuction that return a random int between 1 and 1000
def random_int() -> int:
    return random.randint(1,1000)

#Create a class
@pytest.mark.asyncio
async def create_class(
    async_client: AsyncClient,
) -> int:
    name_class = random_string()

    response: Response = await async_client.post(
        "/api/classes", json={
            "class_name": name_class,
            "key_gbif": random_int(),
        },
    )
    data: Dict[str, Any] = response.json()
    class_id = data["id"]
    return class_id

#Create an order
@pytest.mark.asyncio
async def create_order(
    async_client: AsyncClient,
) -> int:
    name_order = random_string()

    response: Response = await async_client.post(
        "/api/orders", json={
            "order_name": name_order,
            "key_gbif": random_int(),
            "class__id": await create_class(async_client),
        },
    )
    data: Dict[str, Any] = response.json()
    order_id = data["id"]
    return order_id

#Create a family
@pytest.mark.asyncio
async def create_family(
    async_client: AsyncClient,
) -> int:
    name_family = random_string()

    response: Response = await async_client.post(
        "/api/families", json={
            "family_name": name_family,
            "key_gbif": random_int(),
            "order_id": await create_order(async_client),
        },
    )
    data: Dict[str, Any] = response.json()
    family_id = data["id"]
    return family_id

#Create a genus
@pytest.mark.asyncio
async def create_genus(
    async_client: AsyncClient,
) -> int:
    name_genus = random_string()

    response: Response = await async_client.post(
        "/api/genuses", json={
            "genus_name": name_genus,
            "genus_full_name": name_genus,
            "key_gbif": random_int(),
            "family_id": await create_family(async_client),
        },
    )
    data: Dict[str, Any] = response.json()
    genus_id = data["id"]
    return genus_id

#Create a specie
@pytest.mark.asyncio
async def create_specie(
    async_client: AsyncClient,
) -> int:
    name_specie = random_string()


    response: Response = await async_client.post(
        "/api/species", json={
            "scientific_name": name_specie,
            "specific_epithet": name_specie,
            "key_gbif": random_int(),
            "status_id": await create_status_specie(async_client),
            "genus_id": await create_genus(async_client),
        },
    )
    assert response.status_code == 201
    data: Dict[str, Any] = response.json()
    specie_id = data["id"]
    return specie_id

#Create status specie
@pytest.mark.asyncio
async def create_status_specie(
    async_client: AsyncClient,
) -> int:
    name_status_specie = random_string()

    response: Response = await async_client.post(
        "/api/specie/status", json={
            "status_name": name_status_specie,
        },
    )
    data: Dict[str, Any] = response.json()
    status_specie_id = data["id"]
    return status_specie_id


