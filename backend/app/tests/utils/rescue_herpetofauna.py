import random
import string
import pytest
from httpx import Response, AsyncClient
from typing import Dict, Any
from datetime import datetime
from app.tests.conftest import *
from app.tests.utils.towers_example import *
from app.tests.utils.species_example import *


# make a fuction that return a random string of 10 characters
def random_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=10))


# Create a Age Group with name
@pytest.mark.asyncio
async def create_age_groupWithName(
    async_client: AsyncClient,
) -> tuple[int, str]:
    name = random_string()
    response: Response = await async_client.post(
        "/api/age_group", json={
            "name": name
        },
    )
    assert response.status_code == 201
    data = response.json()
    return data["id"], name


# Create a Age Group
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


# Create transect herpetofauna
@pytest.mark.asyncio
async def create_transect_herpetofauna(
    async_client: AsyncClient,
) -> int:
    number_transect: str = random_string()
    tower_id: int = await create_random_tower(async_client)
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


# Create transect herpetofauna with number
@pytest.mark.asyncio
async def create_transect_herpetofaunaWithNumber(
    async_client: AsyncClient,
) -> tuple[int, str]:
    number_transect: str = random_string()
    tower_id: int = await create_random_tower(async_client)
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
    return data["id"], number_transect


# Create a mark herpetofauna
@pytest.mark.asyncio
async def create_mark_herpetofauna(
    async_client: AsyncClient,
) -> int:
    number_mark: int = random.randint(1, 100)
    rescue_herpetofauna_id: int = await create_rescue_herpetofauna(
            async_client
            )

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
            "rescue_herpetofauna_id": rescue_herpetofauna_id
        },
    )
    data = response.json()
    assert response.status_code == 201
    return data["id"]


# Create a mark herpetofauna with number
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
    return data["id"], number_mark


# Create a rescue herpetofauna
@pytest.mark.asyncio
async def create_rescue_herpetofauna(
    async_client: AsyncClient,
) -> int:

    transect_id: int = await create_transect_herpetofauna(async_client)
    number: str = random_string()
    specie_id: int = await create_specie(async_client)
    age_group_id: int = await create_age_group(async_client)

    response: Response = await async_client.post(
        "/api/rescue_herpetofauna", json={
            "number": number,
            "gender": True,
            "specie_id": specie_id,
            "transect_herpetofauna_id": transect_id,
            "age_group_id": age_group_id
        },
    )
    assert response.status_code == 201
    data = response.json()
    return data["id"]


# Create a rescue herpetofauna with number
@pytest.mark.asyncio
async def create_rescue_herpetofaunaWithNumber(
    async_client: AsyncClient,
) -> tuple[int, str]:

    transect_id: int = await create_transect_herpetofauna(async_client)
    number: str = random_string()
    specie_id: int = await create_specie(async_client)
    age_group_id: int = await create_age_group(async_client)

    response: Response = await async_client.post(
        "/api/rescue_herpetofauna", json={
            "number": number,
            "gender": True,
            "specie_id": specie_id,
            "transect_herpetofauna_id": transect_id,
            "age_group_id": age_group_id
        },
    )
    assert response.status_code == 201
    data = response.json()
    return data["id"], number


# Create a transect herpetofauna translocation
@pytest.mark.asyncio
async def create_transect_herpetofauna_translocation(
    async_client: AsyncClient,
) -> int:

    code = random_string()

    response: Response = await async_client.post(
        "/api/transect_herpetofauna_translocation", json={
            "cod": code,
            "date": "2021-10-10T00:00:00",
            "latitude_in": 1.5,
            "longitude_in": 1.5,
            "altitude_in": 15,
            "latitude_out": 1.5,
            "longitude_out": 1.5,
            "altitude_out": 15,
        },
    )

    data = response.json()
    assert response.status_code == 201
    return data["id"]


# Create a transect herpetofauna translocation with code
@pytest.mark.asyncio
async def create_transect_herpetofauna_translocationWithCode(
    async_client: AsyncClient,
) -> tuple[int, str]:

    code = random_string()

    response: Response = await async_client.post(
        "/api/transect_herpetofauna_translocation", json={
            "cod": code,
            "date": "2021-10-10T00:00:00",
            "latitude_in": 1.5,
            "longitude_in": 1.5,
            "altitude_in": 15,
            "latitude_out": 1.5,
            "longitude_out": 1.5,
            "altitude_out": 15,
        },
    )

    data = response.json()
    assert response.status_code == 201
    return data["id"], code


# Create point herpetofauna translocation
@pytest.mark.asyncio
async def create_point_herpetofauna_translocation(
        async_client: AsyncClient,
        ) -> int:

    code = random_string()
    response: Response = await async_client.post(
                "/api/point_herpetofauna_translocation", json={
                    "cod": code,
                    "date": "2021-10-10T00:00:00",
                    "latitude": 1.5,
                    "longitude": 1.5,
                    "altitude": 15,
                    },
                )

    data = response.json()
    assert response.status_code == 201
    return data["id"]


# Create point herpetofauna translocation with code
@pytest.mark.asyncio
async def create_point_herpetofauna_translocation_with_code(
    async_client: AsyncClient,
    ) -> tuple[int, str]:
    code = random_string()

    response: Response = await async_client.post(
            "/api/point_herpetofauna_translocation", json={
                "cod": code,
                "date": "2021-10-10T00:00:00",
                "latitude": 1.5,
                "longitude": 1.5,
                "altitude": 15,
                },
            )

    data = response.json()
    assert response.status_code == 201
    return data["id"], code


# Create a rescue herpetofauna with extra data
@pytest.mark.asyncio
async def create_rescue_herpetofaunaWithExtraData(
    async_client: AsyncClient,
) -> tuple[
        int,
        str,
        datetime,
        datetime,
        float,
        float,
        int,
        float,
        float,
        int,
        str
        ]:

    (
            transect_id,
            number_transect,
            date_in,
            date_out,
            latitude_in,
            longitude_in,
            altitude_in,
            latitude_out,
            longitude_out,

    ) = await create_transect_herpetofaunaWithExtraData(async_client)
    number: str = random_string()
    specie_id, specie_name = await create_specieWithName(async_client)
    age_group_id: int = await create_age_group(async_client)

    response: Response = await async_client.post(
        "/api/rescue_herpetofauna", json={
            "number": number,
            "gender": True,
            "specie_id": specie_id,
            "transect_herpetofauna_id": transect_id,
            "age_group_id": age_group_id
        },
    )
    assert response.status_code == 201
    data = response.json()
    return (
            data["id"],
            number_transect,
            date_in,
            date_out,
            latitude_in,
            longitude_in,
            altitude_in,
            latitude_out,
            longitude_out,
            specie_id,
            specie_name
            )


# Create transect herpetofauna with number
@pytest.mark.asyncio
async def create_transect_herpetofaunaWithExtraData(
    async_client: AsyncClient,
) -> tuple[int, str, datetime, datetime, float, float, int, float, float]:
    number_transect: str = random_string()
    tower_id: int = await create_random_tower(async_client)
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
    return (
            data["id"],
            number_transect,
            data["date_in"],
            data["date_out"],
            latitude_in,
            longitude_in,
            data["altitude_in"],
            latitude_out,
            longitude_out
            )
