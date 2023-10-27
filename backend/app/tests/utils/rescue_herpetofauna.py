import random
import string
import pytest
from httpx import Response, AsyncClient
from typing import Dict, Any
from app.tests.conftest import *
from app.tests.utils.towers_example import *



#make a fuction that return a random string of 10 characters
def random_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=10))


#Create a Age Group with name
@pytest.mark.asyncio
async def create_age_groupWithName(
    async_client: AsyncClient,
) -> tuple[int, str] :
    name = random_string()
    response: Response = await async_client.post(
        "/api/age_group", json={
            "name": name
        },
    )
    assert response.status_code == 201
    data = response.json()
    return data["id"], name

#Create a Age Group
@pytest.mark.asyncio
async def create_age_group(
    async_client: AsyncClient,
) -> int:
    name = random_string()
    response: Response = await async_client.post(
        "/api/age_group", json={
            "name": name
        },
    )
    assert response.status_code == 201
    data = response.json()
    return data["id"]

#Create transect herpetofauna
@pytest.mark.asyncio
async def create_transect_herpetofauna(
    async_client: AsyncClient,
) -> int:
    number_transect: int = random.randint(1, 100)
    tower_id: int =  await create_random_tower(async_client)
    latitude_in: float = random.uniform(-90, 90)
    longitude_in: float = random.uniform(-180, 180)
    latitude_out: float = random.uniform(-90, 90)
    longitude_out: float = random.uniform(-180, 180)

    response: Response = await async_client.post(
        "/api/transect_herpetofauna", json={
            "number": number_transect,
            "date_in": "2021-10-10T00:00:00",
            "date_out": "2021-10-12T00:00:00",
            "latitude_in": latitude_in,
            "longitude_in": longitude_in,
            "altitude_in": 100,
            "latitude_out": latitude_out,
            "longitude_out": longitude_out,
            "altitude_out": 100,
            "tower_id": tower_id
        },
    )
    assert response.status_code == 201
    data = response.json()
    return data["id"]

#Create a mark herpetofauna
@pytest.mark.asyncio
async def create_mark_herpetofauna(
    async_client: AsyncClient,
) -> int:
    number_mark: int = random.randint(1, 100)
    age_group_id:int = await create_age_group(async_client)

    response: Response = await async_client.post(
        "/api/mark_herpetofauna", json={
            "date": "2021-10-10T00:00:00",
            "number": number_mark,
            "code": "123456789",
            "gender": True,
            "LHC": 1.5,
            "weight": 1.5,
            "is_photo_mark": True,
            "is_elastomer_mark": True,
            "age_group_id": age_group_id,
        },
    )
    assert response.status_code == 201
    data = response.json()
    print(f'Response for create mark herpetofauna is : {data}')
    return data["id"]


#Create a mark herpetofauna with number
@pytest.mark.asyncio
async def create_mark_herpetofaunaWithNumber(
    async_client: AsyncClient,
) -> tuple[int, int]:
    number_mark: int = random.randint(1, 100)

    response: Response = await async_client.post(
        "/api/mark_herpetofauna", json={
            "date": "2021-10-10T00:00:00",
            "number": number_mark,
            "code": "123456789",
            "LHC": 1.5,
            "weight": 1.5,
            "is_photo_mark": True,
            "is_elastomer_mark": True,
        },
    )
    assert response.status_code == 201
    data = response.json()
    print(f'Response for create mark herpetofauna is : {data}')
    return data["id"], number_mark
