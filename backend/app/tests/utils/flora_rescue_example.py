import random
import string
import pytest
from httpx import Response, AsyncClient
from app.tests.conftest import *
from app.tests.utils.species_example import *
from app.models.rescue_flora import *


#make a fuction that return a random string of 10 characters
def random_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=10))

#fuctions to create a longitude and latitude
def create_longitude() -> float:
    return random.uniform(-180, 180)

def create_latitude() -> float:
    return random.uniform(-90, 90)


# Create a radom rescue_zone
@pytest.mark.asyncio
async def create_random_rescue_zone_id(
    async_client: AsyncClient
)-> int:
    # create zone rescue
    response = await async_client.post(
        "/api/rescue_flora/rescue_zone", json={
            "name": "test_rescue_zone",
            "description": "test_description",
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    return data["id"]

# Create a radom relocation_zone
@pytest.mark.asyncio
async def create_random_relocation_zone_id(
    async_client: AsyncClient
)-> int:
    response = await async_client.post(
        "/api/rescue_flora/relocation_zone", json={
            "name": "test_relocation_zone0",
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    return data["id"]


# Create a radom rescue_zone with name
@pytest.mark.asyncio
async def create_random_rescue_zone_id_wiht_name(
    async_client: AsyncClient
)-> tuple[int, str]:
    # create zone rescue
    name: str = random_string()
    response = await async_client.post(
        "/api/rescue_flora/rescue_zone", json={
            "name": name,
            "description": "test_description",
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    return data["id"], name

# Create a radom relocation_zone with name
@pytest.mark.asyncio
async def create_random_relocation_zone_idWithNumber(
    async_client: AsyncClient
)-> tuple[int, str]:
    name: str = random_string()
    response = await async_client.post(
        "/api/rescue_flora/relocation_zone", json={
            "name": name,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    return data["id"], name 

@pytest.mark.asyncio
async def create_random_flora_rescue_id(
    async_client: AsyncClient
) -> int:
    epiphyte_number = random_string()
    specie_id = await create_specie(async_client)
    GENUS_ID = await create_genus(async_client)
    FAMILY_ID = await create_family(async_client)
    RESCUE_ZONE_ID = await create_random_rescue_zone_id(async_client)
    # create flora rescue
    response =await async_client.post(
        "/api/rescue_flora", json={
            "epiphyte_number": epiphyte_number,
            "rescue_date": "2021-10-10T00:00:00",
            "rescue_area_latitude": create_latitude(),
            "rescue_area_longitude": create_longitude(),
            "substrate": "test_substrate",
            "dap_bryophyte": 1.0,
            "height_bryophyte": 1.0,
            "bryophyte_position": 1,
            "growth_habit": "test_growth_habit",
            "epiphyte_phenology": "test_epiphyte_phenology",
            "health_status_epiphyte": "test_health_status_epiphyte",
            "microhabitat": "test_microhabitat",
            "other_observations": "test_other_observations",
            "specie_bryophyte_id": specie_id,
            "genus_bryophyte_id": None,
            "family_bryophyte_id": None,
            "specie_epiphyte_id": specie_id,
            "genus_epiphyte_id": None,
            "family_epiphyte_id": None,
            "rescue_zone_id": RESCUE_ZONE_ID,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    return data["id"]

@pytest.mark.asyncio
async def create_random_flora_rescue_idWithNumber(
    async_client: AsyncClient
) -> tuple[int, str]:
    epiphyte_number = random_string()
    specie_id = await create_specie(async_client)
    GENUS_ID = await create_genus(async_client)
    FAMILY_ID = await create_family(async_client)
    RESCUE_ZONE_ID = await create_random_rescue_zone_id(async_client)
    # create flora rescue
    response =await async_client.post(
        "/api/rescue_flora", json={
            "epiphyte_number": epiphyte_number,
            "rescue_date": "2021-10-10T00:00:00",
            "rescue_area_latitude": create_latitude(),
            "rescue_area_longitude": create_longitude(),
            "substrate": "test_substrate",
            "dap_bryophyte": 1.0,
            "height_bryophyte": 1.0,
            "bryophyte_position": 1,
            "growth_habit": "test_growth_habit",
            "epiphyte_phenology": "test_epiphyte_phenology",
            "health_status_epiphyte": "test_health_status_epiphyte",
            "microhabitat": "test_microhabitat",
            "other_observations": "test_other_observations",
            "specie_bryophyte_id": specie_id,
            "genus_bryophyte_id": None,
            "family_bryophyte_id": None,
            "specie_epiphyte_id": specie_id,
            "genus_epiphyte_id": None,
            "family_epiphyte_id": None,
            "rescue_zone_id": RESCUE_ZONE_ID,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    return data["id"], epiphyte_number


@pytest.mark.asyncio
async def create_random_flora_rescue_WithNumberSpecie(
    async_client: AsyncClient
) -> tuple[int, str, str]:
    epiphyte_number = random_string()
    specie_id, specie = await create_specieWithName(async_client)
    GENUS_ID = await create_genus(async_client)
    FAMILY_ID = await create_family(async_client)
    RESCUE_ZONE_ID = await create_random_rescue_zone_id(async_client)
    # create flora rescue
    response =await async_client.post(
        "/api/rescue_flora", json={
            "epiphyte_number": epiphyte_number,
            "rescue_date": "2021-10-10T00:00:00",
            "rescue_area_latitude": create_latitude(),
            "rescue_area_longitude": create_longitude(),
            "substrate": "test_substrate",
            "dap_bryophyte": 1.0,
            "height_bryophyte": 1.0,
            "bryophyte_position": 1,
            "growth_habit": "test_growth_habit",
            "epiphyte_phenology": "test_epiphyte_phenology",
            "health_status_epiphyte": "test_health_status_epiphyte",
            "microhabitat": "test_microhabitat",
            "other_observations": "test_other_observations",
            "specie_bryophyte_id": specie_id,
            "genus_bryophyte_id": None,
            "family_bryophyte_id": None,
            "specie_epiphyte_id": specie_id,
            "genus_epiphyte_id": None,
            "family_epiphyte_id": None,
            "rescue_zone_id": RESCUE_ZONE_ID,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    return data["id"], epiphyte_number, specie
