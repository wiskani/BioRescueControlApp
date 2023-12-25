import random
import string
import pytest
from httpx import Response, AsyncClient
from typing import Dict, Any
from app.tests.conftest import *
from app.tests.utils.species_example import *
from app.tests.utils.rescue_herpetofauna import *

#generate radom habitat
@pytest.mark.asyncio
async def create_habitat(
    async_client: AsyncClient,
) -> int:
    name_habitat = random_string()

    response = await async_client.post(
        "api/habitat", json={
            "name": name_habitat
        },
    )
    data = response.json()
    assert response.status_code == 201
    return data["id"]

#generate radom habitat with name
@pytest.mark.asyncio
async def create_habitatWithName(
    async_client: AsyncClient,
) -> tuple[int, str]:
    name_habitat = random_string()

    response = await async_client.post(
        "api/habitat", json={
            "name": name_habitat
        },
    )
    data = response.json()
    assert response.status_code == 201
    return data["id"], name_habitat

#generate radom rescue mammals
@pytest.mark.asyncio
async def create_rescue_mammals(
    async_client: AsyncClient,
) -> int:
    habitat_id = await create_habitat(async_client)
    age_group_id = await create_age_group(async_client)
    specie_id = await create_specie(async_client)
    cod = random_string()

    response = await async_client.post(
        "api/rescue_mammals", json={
            "cod": cod,
            "date": "2021-10-10T00:00:00",
            "mark": "mark",
            "longitude": 1.0,
            "latitude": 1.0,
            "altitude": 10,
            "gender": True,
            "LT": 1.0,
            "LC": 1.0,
            "LP": 1.0,
            "LO": 1.0,
            "LA": 1.0,
            "weight": 10,
            "observation": "observation",
            "is_specie_confirmed": True,
            "habitat_id": habitat_id,
            "age_group_id": age_group_id,
            "specie_id": specie_id,
            "genus_id": None
        },
    )
    data = response.json()
    assert response.status_code == 201
    return data["id"]

#generate radom rescue mammals with cod
@pytest.mark.asyncio
async def create_rescue_mammalsWithCod(
    async_client: AsyncClient,
) -> tuple[int, str]:
    habitat_id = await create_habitat(async_client)
    age_group_id = await create_age_group(async_client)
    specie_id = await create_specie(async_client)
    cod = random_string()

    response = await async_client.post(
        "api/rescue_mammals", json={
            "cod": cod,
            "date": "2021-10-10T00:00:00",
            "mark": "mark",
            "longitude": 1.0,
            "latitude": 1.0,
            "altitude": 10,
            "gender": True,
            "LT": 1.0,
            "LC": 1.0,
            "LP": 1.0,
            "LO": 1.0,
            "LA": 1.0,
            "weight": 10,
            "observation": "observation",
            "is_specie_confirmed": True,
            "habitat_id": habitat_id,
            "age_group_id": age_group_id,
            "specie_id": specie_id,
            "genus_id": None
        },
    )
    data = response.json()
    assert response.status_code == 201
    return data["id"], cod

#generate radom rescue mammals with cod
@pytest.mark.asyncio
async def create_rescue_mammalsWithCodSpecieGenus(
    async_client: AsyncClient,
) -> tuple[int, str, str|None, int|None, str|None, int|None]:
    habitat_id = await create_habitat(async_client)
    age_group_id = await create_age_group(async_client)
    specie_id, specie_name = await create_specieWithName(async_client)
    cod = random_string()

    response = await async_client.post(
        "api/rescue_mammals", json={
            "cod": cod,
            "date": "2021-10-10T00:00:00",
            "mark": "mark",
            "longitude": 1.0,
            "latitude": 1.0,
            "altitude": 10,
            "gender": True,
            "LT": 1.0,
            "LC": 1.0,
            "LP": 1.0,
            "LO": 1.0,
            "LA": 1.0,
            "weight": 10,
            "observation": "observation",
            "is_specie_confirmed": True,
            "habitat_id": habitat_id,
            "age_group_id": age_group_id,
            "specie_id": specie_id,
            "genus_id": None
        },
    )
    data = response.json()
    assert response.status_code == 201
    return data["id"], cod, specie_name, specie_id, None, None

#generate radom site release
@pytest.mark.asyncio
async def create_site_release(
    async_client: AsyncClient,
) -> int:
    name_site_release = random_string()

    response = await async_client.post(
        "api/site_release_mammals", json={
            "name": name_site_release
        },
    )
    data = response.json()
    assert response.status_code == 201
    return data["id"]

#generate radom site release with name
@pytest.mark.asyncio
async def create_site_releaseWithName(
    async_client: AsyncClient,
) -> tuple[int, str]:
    name_site_release = random_string()

    response = await async_client.post(
        "api/site_release_mammals", json={
            "name": name_site_release
        },
    )
    data = response.json()
    assert response.status_code == 201
    return data["id"], name_site_release
