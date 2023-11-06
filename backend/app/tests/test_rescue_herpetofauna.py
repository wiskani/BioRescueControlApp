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
TEST CRUD FOR TRANSECT HERPETOFAUNA
"""

#test create transect herpetofauna
@pytest.mark.asyncio
async def test_create_transect_herpetofauna(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    number_transect: int = random_string()
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
    assert data["number"] == number_transect
    assert data["latitude_in"] == latitude_in
    assert data["longitude_in"] == longitude_in
    assert data["latitude_out"] == latitude_out
    assert data["longitude_out"] == longitude_out
    assert "id" in data

#test get create transect herpetofauna with invalid number
@pytest.mark.asyncio
async def test_create_transect_herpetofauna_with_invalid_number(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    number_transect: int = random_string()
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
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Transect herpetofauna number already exists"

#test get transect herpetofauna by id
@pytest.mark.asyncio
async def test_get_transect_herpetofauna_by_id(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    number_transect: int = random_string()
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
    transect_herpetofauna_id: int = data["id"]

    response: Response = await async_client.get(
        f"/api/transect_herpetofauna/{transect_herpetofauna_id}"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["number"] == number_transect
    assert data["latitude_in"] == latitude_in
    assert data["longitude_in"] == longitude_in
    assert data["latitude_out"] == latitude_out
    assert data["longitude_out"] == longitude_out
    assert data["tower_id"] == tower_id

#test get transect herpetofauna by id with invalid id
@pytest.mark.asyncio
async def test_get_transect_herpetofauna_by_id_with_invalid_id(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    response: Response = await async_client.get(
        f"/api/transect_herpetofauna/{random.randint(1, 100)}"
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Transect herpetofauna not found"

#test get all transect herpetofauna
@pytest.mark.asyncio
async def test_get_all_transect_herpetofauna(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    number_transect: int = random_string()
    tower_id: int =  await create_random_tower(async_client)
    latitude_in: float = random.uniform(-90, 90)
    longitude_in: float = random.uniform(-180, 180)
    latitude_out: float = random.uniform(-90, 90)
    longitude_out: float = random.uniform(-180, 180)

    number_transect_2: int = random_string()
    tower_id_2: int =  await create_random_tower(async_client)
    latitude_in_2: float = random.uniform(-90, 90)
    longitude_in_2: float = random.uniform(-180, 180)
    latitude_out_2: float = random.uniform(-90, 90)
    longitude_out_2: float = random.uniform(-180, 180)

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

    response: Response = await async_client.post(
        "/api/transect_herpetofauna", json={
            "number": number_transect_2,
            "date_in": "2021-10-10T00:00:00",
            "date_out": "2021-10-12T00:00:00",
            "latitude_in": latitude_in_2,
            "longitude_in": longitude_in_2,
            "altitude_in": 100,
            "latitude_out": latitude_out_2,
            "longitude_out": longitude_out_2,
            "altitude_out": 100,
            "tower_id": tower_id_2
        },
    )
    assert response.status_code == 201

    response: Response = await async_client.get(
        f"/api/transect_herpetofauna"
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

#test update transect herpetofauna
@pytest.mark.asyncio
async def test_update_transect_herpetofauna(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    number_transect: int = random_string()
    tower_id: int =  await create_random_tower(async_client)
    latitude_in: float = random.uniform(-90, 90)
    longitude_in: float = random.uniform(-180, 180)
    latitude_out: float = random.uniform(-90, 90)
    longitude_out: float = random.uniform(-180, 180)

    number_transect_2: int = random_string()
    tower_id_2: int =  await create_random_tower(async_client)
    latitude_in_2: float = random.uniform(-90, 90)
    longitude_in_2: float = random.uniform(-180, 180)
    latitude_out_2: float = random.uniform(-90, 90)
    longitude_out_2: float = random.uniform(-180, 180)

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
    number_transect_id: int = data["id"]

    response: Response = await async_client.put(
        f"/api/transect_herpetofauna/{number_transect_id}", json={
            "number": number_transect_2,
            "date_in": "2021-10-10T00:00:00",
            "date_out": "2021-10-12T00:00:00",
            "latitude_in": latitude_in_2,
            "longitude_in": longitude_in_2,
            "altitude_in": 100,
            "latitude_out": latitude_out_2,
            "longitude_out": longitude_out_2,
            "altitude_out": 100,
            "tower_id": tower_id_2
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["number"] == number_transect_2
    assert data["latitude_in"] == latitude_in_2
    assert data["longitude_in"] == longitude_in_2
    assert data["latitude_out"] == latitude_out_2
    assert data["longitude_out"] == longitude_out_2
    assert data["tower_id"] == tower_id_2

#test delete transect herpetofauna
@pytest.mark.asyncio
async def test_delete_transect_herpetofauna(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    number_transect: int = random_string()
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
    number_transect_id: int = data["id"]

    response: Response = await async_client.delete(
        f"/api/transect_herpetofauna/{number_transect_id}"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["detail"] == "Transect herpetofauna deleted successfully"







"""
TEST CRUD FOR MARK HERPETOFAUNA
"""

#test create mark herpetofauna
@pytest.mark.asyncio
async def test_create_mark_herpetofauna(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    number_mark: int = random.randint(1, 100)
    rescue_herpetofauna_id : int = await create_rescue_herpetofauna(async_client)

    response: Response = await async_client.post(
        "/api/mark_herpetofauna", json={
            "date": "2021-10-10T00:00:00",
            "number": number_mark,
            "code": "123456789",
            "LHC": 1.5,
            "weight": 1.5,
            "is_photo_mark": True,
            "is_elastomer_mark": True,
            "rescue_herpetofauna_id": rescue_herpetofauna_id
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["number"] == number_mark
    assert "id" in data

#test create mark herpetofauna with tower not found
@pytest.mark.asyncio
async def test_create_mark_herpetofauna_with_tower_not_found(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    number_mark: int = random.randint(1, 100)
    rescue_herpetofauna_id: int = await create_rescue_herpetofauna(async_client)

    response: Response = await async_client.post(
        "/api/mark_herpetofauna", json={
            "date": "2021-10-10T00:00:00",
            "number": number_mark,
            "code": "123456789",
            "LHC": 1.5,
            "weight": 1.5,
            "is_photo_mark": True,
            "is_elastomer_mark": True,
            "rescue_herpetofauna_id": rescue_herpetofauna_id
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["number"] == number_mark
    assert "id" in data

    response: Response = await async_client.post(
        "/api/mark_herpetofauna", json={
            "date": "2021-10-10T00:00:00",
            "number": number_mark,
            "code": "123456789",
            "LHC": 1.5,
            "weight": 1.5,
            "is_photo_mark": True,
            "is_elastomer_mark": True,
            "rescue_herpetofauna_id": rescue_herpetofauna_id
        },
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Mark herpetofauna number already exists"

#test get all mark herpetofauna
@pytest.mark.asyncio
async def test_get_all_mark_herpetofauna(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    number_mark: int = random.randint(1, 100)
    rescue_herpetofauna_id : int = await create_rescue_herpetofauna(async_client)

    number_mark_2: int = random.randint(1, 100)
    rescue_herpetofauna_id2 : int = await create_rescue_herpetofauna(async_client)

    response: Response = await async_client.post(
        "/api/mark_herpetofauna", json={
            "date": "2021-10-10T00:00:00",
            "number": number_mark,
            "code": "123456789",
            "LHC": 1.5,
            "weight": 1.5,
            "is_photo_mark": True,
            "is_elastomer_mark": True,
            "rescue_herpetofauna_id": rescue_herpetofauna_id

        },
    )
    assert response.status_code == 201

    response: Response = await async_client.post(
        "/api/mark_herpetofauna", json={
            "date": "2021-10-10T00:00:00",
            "number": number_mark_2,
            "code": "123456789b",
            "LHC": 1.5,
            "weight": 1.5,
            "is_photo_mark": True,
            "is_elastomer_mark": True,
            "rescue_herpetofauna_id": rescue_herpetofauna_id2
        },
    )
    assert response.status_code == 201

    response: Response = await async_client.get(
        "/api/mark_herpetofauna",
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

#test get mark herpetofauna by id
@pytest.mark.asyncio
async def test_get_mark_herpetofauna_by_id(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    number_mark: int = random.randint(1, 100)
    rescue_herpetofauna_id : int = await create_rescue_herpetofauna(async_client)

    response: Response = await async_client.post(
        "/api/mark_herpetofauna", json={
            "date": "2021-10-10T00:00:00",
            "number": number_mark,
            "code": "123456789",
            "LHC": 1.5,
            "weight": 1.5,
            "is_photo_mark": True,
            "is_elastomer_mark": True,
            "rescue_herpetofauna_id": rescue_herpetofauna_id
        },
    )
    assert response.status_code == 201
    data = response.json()
    mark_herpetofauna_id = data["id"]

    response: Response = await async_client.get(
        f"/api/mark_herpetofauna/{mark_herpetofauna_id}",
    )
    assert response.status_code == 200
    data = response.json()
    assert data["number"] == number_mark

#test get mark herpetofauna by id not found
@pytest.mark.asyncio
async def test_get_mark_herpetofauna_by_id_not_found(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    response: Response = await async_client.get(
        f"/api/mark_herpetofauna/0",
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Mark herpetofauna not found"

#test update mark herpetofauna
@pytest.mark.asyncio
async def test_update_mark_herpetofauna(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    number_mark: int = random.randint(1, 100)
    rescue_herpetofauna_id : int = await create_rescue_herpetofauna(async_client)

    number_mark_2: int = random.randint(1, 100)
    rescue_herpetofauna_id_2 : int = await create_rescue_herpetofauna(async_client)

    response: Response = await async_client.post(
        "/api/mark_herpetofauna", json={
            "date": "2021-10-10T00:00:00",
            "number": number_mark,
            "code": "123456789",
            "LHC": 1.5,
            "weight": 1.5,
            "is_photo_mark": True,
            "is_elastomer_mark": True,
            "rescue_herpetofauna_id": rescue_herpetofauna_id
        },
    )
    assert response.status_code == 201
    data = response.json()
    mark_herpetofauna_id = data["id"]

    response: Response = await async_client.put(
        f"/api/mark_herpetofauna/{mark_herpetofauna_id}", json={
            "date": "2021-10-10T00:00:00",
            "number": number_mark_2,
            "code": "123456789b",
            "LHC": 1.5,
            "weight": 1.5,
            "is_photo_mark": True,
            "is_elastomer_mark": True,
            "rescue_herpetofauna_id": rescue_herpetofauna_id_2
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["number"] == number_mark_2

#test for delete mark herpetofauna
@pytest.mark.asyncio
async def test_delete_mark_herpetofauna(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    number_mark: int = random.randint(1, 100)
    resuce_herpetofauna_id : int = await create_rescue_herpetofauna(async_client)

    response: Response = await async_client.post(
        "/api/mark_herpetofauna", json={
            "date": "2021-10-10T00:00:00",
            "number": number_mark,
            "code": "123456789",
            "LHC": 1.5,
            "weight": 1.5,
            "is_photo_mark": True,
            "is_elastomer_mark": True,
            "rescue_herpetofauna_id": resuce_herpetofauna_id
        },
    )
    assert response.status_code == 201
    data = response.json()
    mark_herpetofauna_id = data["id"]

    response: Response = await async_client.delete(
        f"/api/mark_herpetofauna/{mark_herpetofauna_id}",
    )
    assert response.status_code == 200
    data = response.json()
    assert data["detail"] == "Mark herpetofauna deleted successfully"

"""
TEST FOR CRUD RESCUE HERPETOFAUNA
"""

#test create rescue herpetofauna
@pytest.mark.asyncio
async def test_create_rescue_herpetofauna(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    number_rescue: int = random_string()
    specie_id:int = await create_specie(async_client)
    transect_herpetofauna_id:int = await create_transect_herpetofauna(async_client)
    age_group_id:int = await create_age_group(async_client)

    response: Response = await async_client.post(
        "/api/rescue_herpetofauna", json={
            "number": number_rescue,
            "gender": True,
            "specie_id": specie_id,
            "transect_herpetofauna_id": transect_herpetofauna_id,
            "age_group_id": age_group_id,
        },
    )
    data = response.json()
    print(f'La respuesta es {data}')
    assert response.status_code == 201
    assert data["number"] == number_rescue
    assert data["gender"] == True
    assert data["specie_id"] == specie_id
    assert data["transect_herpetofauna_id"] == transect_herpetofauna_id
    assert data["age_group_id"] == age_group_id

#test get rescue herpetofauna by id
@pytest.mark.asyncio
async def test_get_rescue_herpetofauna_by_id(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    number_rescue: int = random_string()
    specie_id:int = await create_specie(async_client)
    transect_herpetofauna_id:int = await create_transect_herpetofauna(async_client)
    age_group_id:int = await create_age_group(async_client)

    response: Response = await async_client.post(
        "/api/rescue_herpetofauna", json={
            "number": number_rescue,
            "gender": True,
            "specie_id": specie_id,
            "transect_herpetofauna_id": transect_herpetofauna_id,
            "age_group_id": age_group_id,
        },
    )
    assert response.status_code == 201
    data = response.json()
    rescue_herpetofauna_id = data["id"]

    response: Response = await async_client.get(
        f"/api/rescue_herpetofauna/{rescue_herpetofauna_id}",
    )
    assert response.status_code == 200
    data = response.json()
    assert data["number"] == number_rescue
    assert data["gender"] == True
    assert data["specie_id"] == specie_id
    assert data["transect_herpetofauna_id"] == transect_herpetofauna_id
    assert data["age_group_id"] == age_group_id

#test for create rescue herpetofauna with wrong number
@pytest.mark.asyncio
async def test_create_rescue_herpetofauna_with_wrong_number(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    number_rescue: int = random_string()
    specie_id:int = await create_specie(async_client)
    transect_herpetofauna_id:int = await create_transect_herpetofauna(async_client)
    age_group_id:int = await create_age_group(async_client)

    response: Response = await async_client.post(
        "/api/rescue_herpetofauna", json={
            "number": number_rescue,
            "gender": True,
            "specie_id": specie_id,
            "transect_herpetofauna_id": transect_herpetofauna_id,
            "age_group_id": age_group_id,
        },
    )
    assert response.status_code == 201
    data = response.json()

    response: Response = await async_client.post(
        "/api/rescue_herpetofauna", json={
            "number": number_rescue,
            "gender": True,
            "specie_id": specie_id,
            "transect_herpetofauna_id": transect_herpetofauna_id,
            "age_group_id": age_group_id,
        },
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Rescue herpetofauna number already exists"

#test for get all rescue herpetofauna
@pytest.mark.asyncio
async def test_get_all_rescue_herpetofauna(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    number_rescue: int = random_string()
    specie_id:int = await create_specie(async_client)
    transect_herpetofauna_id:int = await create_transect_herpetofauna(async_client)
    age_group_id:int = await create_age_group(async_client)

    response: Response = await async_client.post(
        "/api/rescue_herpetofauna", json={
            "number": number_rescue,
            "gender": True,
            "specie_id": specie_id,
            "transect_herpetofauna_id": transect_herpetofauna_id,
            "age_group_id": age_group_id,
        },
    )
    assert response.status_code == 201
    data = response.json()

    response: Response = await async_client.get(
        "/api/rescue_herpetofauna",
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

#test for update rescue herpetofauna
@pytest.mark.asyncio
async def test_update_rescue_herpetofauna(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    number_rescue: str = random_string()
    specie_id:int = await create_specie(async_client)
    transect_herpetofauna_id:int = await create_transect_herpetofauna(async_client)
    age_group_id:int = await create_age_group(async_client)

    number_rescue_update: str = random_string()
    specie_id_update:int = await create_specie(async_client)
    age_group_id_update:int = await create_age_group(async_client)


    response: Response = await async_client.post(
        "/api/rescue_herpetofauna", json={
            "number": number_rescue,
            "gender": True,
            "specie_id": specie_id,
            "transect_herpetofauna_id": transect_herpetofauna_id,
            "age_group_id": age_group_id,
        },
    )
    assert response.status_code == 201
    data = response.json()
    rescue_herpetofauna_id = data["id"]

    response: Response = await async_client.put(
        f"/api/rescue_herpetofauna/{rescue_herpetofauna_id}", json={
            "number": number_rescue_update,
            "gender": True,
            "specie_id": specie_id_update,
            "transect_herpetofauna_id": transect_herpetofauna_id,
            "age_group_id": age_group_id_update,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["number"] == number_rescue_update
    assert data["gender"] == True
    assert data["specie_id"] == specie_id_update
    assert data["transect_herpetofauna_id"] == transect_herpetofauna_id
    assert data["age_group_id"] == age_group_id_update

#test for delete rescue herpetofauna
@pytest.mark.asyncio
async def test_delete_rescue_herpetofauna(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    number_rescue: str = random_string()
    specie_id:int = await create_specie(async_client)
    transect_herpetofauna_id:int = await create_transect_herpetofauna(async_client)
    age_group_id:int = await create_age_group(async_client)

    response: Response = await async_client.post(
        "/api/rescue_herpetofauna", json={
            "number": number_rescue,
            "gender": True,
            "specie_id": specie_id,
            "transect_herpetofauna_id": transect_herpetofauna_id,
            "age_group_id": age_group_id,
        },
    )
    assert response.status_code == 201
    data = response.json()
    rescue_herpetofauna_id = data["id"]

    response: Response = await async_client.delete(
        f"/api/rescue_herpetofauna/{rescue_herpetofauna_id}",
    )
    assert response.status_code == 200
    data = response.json()
    assert data["detail"] == "Rescue herpetofauna deleted successfully"

"""
TESTS FOR CRUD TRANSECT HERPETOFAUNA TRANSLOCATION
"""

#test for create transect herpetofauna translocation
@pytest.mark.asyncio
async def test_create_transect_herpetofauna_translocation(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:

    code= random_string()

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
    assert "id" in data
    assert data["cod"] == code
    assert data["latitude_in"] == 1.5
    assert data["longitude_in"] == 1.5
    assert data["altitude_in"] == 15
    assert data["latitude_out"] == 1.5
    assert data["longitude_out"] == 1.5
    assert data["altitude_out"] == 15

#Test for get all transect herpetofauna translocation
@pytest.mark.asyncio
async def test_get_all_transect_herpetofauna_translocation(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:

    #Create two transect herpetofauna translocation
    code1 = random_string()
    code2 = random_string()

    response: Response = await async_client.post(
        "/api/transect_herpetofauna_translocation", json={
            "cod": code1,
            "date": "2021-10-10T00:00:00",
            "latitude_in": 1.5,
            "longitude_in": 1.5,
            "altitude_in": 15,
            "latitude_out": 1.5,
            "longitude_out": 1.5,
            "altitude_out": 15,
        },
    )

    assert response.status_code == 201

    response: Response = await async_client.post(
        "/api/transect_herpetofauna_translocation", json={
            "cod": code2,
            "date": "2021-10-10T00:00:00",
            "latitude_in": 1.5,
            "longitude_in": 1.5,
            "altitude_in": 15,
            "latitude_out": 1.5,
            "longitude_out": 1.5,
            "altitude_out": 15,
        },
    )

    assert response.status_code == 201

    #Get two transect herpetofauna translocation
    response: Response = await async_client.get(
        "/api/transect_herpetofauna_translocation",
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

#Test for get transect herpetofauna translocation by id
@pytest.mark.asyncio
async def test_get_transect_herpetofauna_translocation_by_id(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    #Create transect herpetofauna translocation
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

    assert response.status_code == 201
    data = response.json()
    transect_herpetofauna_translocation_id = data["id"]

    #Get transect herpetofauna translocation by id
    response: Response = await async_client.get(
        f"/api/transect_herpetofauna_translocation/{transect_herpetofauna_translocation_id}",
    )
    assert response.status_code == 200
    data = response.json()
    assert data["cod"] == code

#Test for update transect herpetofauna translocation
@pytest.mark.asyncio
async def test_update_transect_herpetofauna_translocation(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    
    #Create transect herpetofauna translocation
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

    assert response.status_code == 201
    data = response.json()
    transect_herpetofauna_translocation_id = data["id"]

    #Update transect herpetofauna translocation

    code_update = random_string()

    response: Response = await async_client.put(
        f"/api/transect_herpetofauna_translocation/{transect_herpetofauna_translocation_id}", json={
            "cod": code_update,
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
    print(f'La respuesta es {data}')
    assert response.status_code == 200
    assert data["cod"] == code_update

#Test for delete transect herpetofauna translocation
@pytest.mark.asyncio
async def test_delete_transect_herpetofauna_translocation(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    #Create transect herpetofauna translocation
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

    assert response.status_code == 201
    data = response.json()
    transect_herpetofauna_translocation_id = data["id"]

    #delete transect herpetofauna translocation
    response: Response = await async_client.delete(
        f"/api/transect_herpetofauna_translocation/{transect_herpetofauna_translocation_id}",
    )
    assert response.status_code == 200
    data = response.json()
    assert data["detail"] == "Transect herpetofauna translocation deleted successfully"

"""
TESTS FOR CRUD POINT HERPETOFAUNA TRANSLOCATION
"""

#Test for create point herpetofauna translocation
@pytest.mark.asyncio
async def test_create_point_herpetofauna_translocation(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:

        code= random_string()

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
        assert "id" in data
        assert data["cod"] == code
        assert data["latitude"] == 1.5
        assert data["longitude"] == 1.5
        assert data["altitude"] == 15

#Test for get all point herpetofauna translocation
@pytest.mark.asyncio
async def test_get_all_point_herpetofauna_translocation(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    # create two point herpetofauna translocation
    code1 = random_string()
    code2 = random_string()

    response: Response = await async_client.post(
        "/api/point_herpetofauna_translocation", json={
            "cod": code1,
            "date": "2021-10-10T00:00:00",
            "latitude": 1.5,
            "longitude": 1.5,
            "altitude": 15,
        },
    )
    assert response.status_code == 201

    response: Response = await async_client.post(
        "/api/point_herpetofauna_translocation", json={
            "cod": code2,
            "date": "2021-10-10T00:00:00",
            "latitude": 1.5,
            "longitude": 1.5,
            "altitude": 15,
        },
    )
    assert response.status_code == 201

    #Get two point herpetofauna translocation
    response: Response = await async_client.get(
        "/api/point_herpetofauna_translocation",
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

#Test for get point herpetofauna translocation by id
@pytest.mark.asyncio
async def test_get_point_herpetofauna_translocation_by_id(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    #Create point herpetofauna translocation
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
    assert response.status_code == 201
    data = response.json()
    point_herpetofauna_translocation_id = data["id"]

    #Get point herpetofauna translocation by id
    response: Response = await async_client.get(
        f"/api/point_herpetofauna_translocation/{point_herpetofauna_translocation_id}",
    )
    assert response.status_code == 200
    data = response.json()
    assert data["cod"] == code

#Update point herpetofauna translocation
@pytest.mark.asyncio
async def test_update_point_herpetofauna_translocation(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    #Create point herpetofauna translocation
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
    assert response.status_code == 201
    data = response.json()
    point_herpetofauna_translocation_id = data["id"]

    #Update point herpetofauna translocation
    code_update = random_string()

    response: Response = await async_client.put(
        f"/api/point_herpetofauna_translocation/{point_herpetofauna_translocation_id}", json={
            "cod": code_update,
            "date": "2021-10-10T00:00:00",
            "latitude": 1.5,
            "longitude": 1.5,
            "altitude": 15,
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data["cod"] == code_update

#Test delete point herpetofauna translocation
@pytest.mark.asyncio
async def test_delete_point_herpetofauna_translocation(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    #Create point herpetofauna translocation
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
    assert response.status_code == 201
    data = response.json()
    point_herpetofauna_translocation_id = data["id"]

    #Delete point herpetofauna translocation
    response: Response = await async_client.delete(
        f"/api/point_herpetofauna_translocation/{point_herpetofauna_translocation_id}",
    )
    assert response.status_code == 200
    data = response.json()
    assert data["detail"] == "Point herpetofauna translocation deleted successfully"

"""
TESTS FOR CRUD TRANLOCATION HERPETOFAUNA
"""

#Test for create translocation herpetofauna
@pytest.mark.asyncio
async def test_create_translocation_herpetofauna(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    #Create specie_id
    specie_id = await create_specie(async_client)
    #Create transect herpetofauna translocation
    transect_herpetofauna_translocation_id : int = await create_transect_herpetofauna_translocation(async_client)
    #Create point herpetofauna translocation 
    point_herpetofauna_translocation_id : int = await create_point_herpetofauna_translocation(async_client)
    #Create mark herpetofauna
    mark_herpetofauna_id : int = await create_mark_herpetofauna(async_client)

    code = random_string()

    #Create translocation herpetofauna
    response: Response = await async_client.post(
        "/api/translocation_herpetofauna", json={
            "cod": code,
            "transect_herpetofauna_translocation_id": transect_herpetofauna_translocation_id,
            "point_herpetofauna_translocation_id": point_herpetofauna_translocation_id,
            "specie_id": specie_id,
            "mark_herpetofauna_id": mark_herpetofauna_id,
        },
    )

    data = response.json()
    print(f"La respuesta es {data}")
    assert response.status_code == 201
    assert data["cod"] == code
    assert data["transect_herpetofauna_translocation_id"]== transect_herpetofauna_translocation_id
    assert data["point_herpetofauna_translocation_id"] == point_herpetofauna_translocation_id
    assert data["specie_id"] == specie_id
    assert data["mark_herpetofauna_id"] == mark_herpetofauna_id

#Test for get all translocation herpetofauna
@pytest.mark.asyncio
async def test_get_all_translocation_herpetofauna(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    #Create two translocation herpetofauna
    specie_id = await create_specie(async_client)
    transect_herpetofauna_translocation_id : int = await create_transect_herpetofauna_translocation(async_client)
    point_herpetofauna_translocation_id: int = await create_point_herpetofauna_translocation(async_client)
    mark_herpetofauna_id: int = await create_mark_herpetofauna(async_client)
    code = random_string()
    code2= random_string()

    response: Response = await async_client.post(
        "/api/translocation_herpetofauna", json={
            "cod": code,
            "transect_herpetofauna_translocation_id": transect_herpetofauna_translocation_id,
            "point_herpetofauna_translocation_id": None,
            "specie_id": specie_id,
            "mark_herpetofauna_id": mark_herpetofauna_id,
        },
    )
    assert response.status_code == 201

    response: Response = await async_client.post(
        "/api/translocation_herpetofauna", json={
            "cod": code2,
            "transect_herpetofauna_translocation_id": None,
            "point_herpetofauna_translocation_id": point_herpetofauna_translocation_id,
            "specie_id": specie_id,
            "mark_herpetofauna_id": mark_herpetofauna_id,
        },
    )
    assert response.status_code == 201

    #get all translocation herpetofauna
    response: Response = await async_client.get(
        "/api/translocation_herpetofauna",
    )
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2

#Test for get translocation herpetofauna by id
@pytest.mark.asyncio
async def test_get_translocation_herpetofauna_by_id(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    #create a translocation herpetofauna
    specie_id = await create_specie(async_client)
    transect_herpetofauna_translocation_id : int = await create_transect_herpetofauna_translocation(async_client)
    mark_herpetofauna_id: int = await create_mark_herpetofauna(async_client)
    
    code = random_string()

    response: Response = await async_client.post(
        "/api/translocation_herpetofauna", json={
            "cod": code,
            "transect_herpetofauna_translocation_id": transect_herpetofauna_translocation_id,
            "point_herpetofauna_translocation_id": None,
            "specie_id": specie_id,
            "mark_herpetofauna_id": mark_herpetofauna_id,
        },
    )
    data = response.json()
    assert response.status_code == 201
    translocation_herpetofauna_id = data["id"]

    #get translocation herpetofauna by id
    response: Response = await async_client.get(
        f"/api/translocation_herpetofauna/{translocation_herpetofauna_id}",
    )
    data = response.json()
    assert response.status_code == 200
    assert data["cod"] == code
    assert data["transect_herpetofauna_translocation_id"] == transect_herpetofauna_translocation_id
    assert data["point_herpetofauna_translocation_id"] == None

#Test for update translocation herpetofauna
@pytest.mark.asyncio
async def test_update_translocation_herpetofauna(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    #Create a translocation herpetofauna
    specie_id = await create_specie(async_client)
    transect_herpetofauna_translocation_id : int = await create_transect_herpetofauna_translocation(async_client)
    point_herpetofauna_translocation_id:int = await create_point_herpetofauna_translocation(async_client)
    mark_herpetofauna_id: int = await create_mark_herpetofauna(async_client)
    code = random_string()

    response: Response = await async_client.post(
        "/api/translocation_herpetofauna", json={
            "cod": code,
            "transect_herpetofauna_translocation_id": transect_herpetofauna_translocation_id,
            "point_herpetofauna_translocation_id": None,
            "specie_id": specie_id,
            "mark_herpetofauna_id": mark_herpetofauna_id,
        },
    )
    data = response.json()
    assert response.status_code == 201
    translocation_herpetofauna_id = data["id"]

    #update translocation herpetofauna
    code2 = random_string()
    response: Response = await async_client.put(
        f"/api/translocation_herpetofauna/{translocation_herpetofauna_id}", json={
            "cod": code2,
            "transect_herpetofauna_translocation_id": None,
            "point_herpetofauna_translocation_id": point_herpetofauna_translocation_id,
            "specie_id": specie_id,
            "mark_herpetofauna_id": mark_herpetofauna_id,
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data["cod"] == code2
    assert data["transect_herpetofauna_translocation_id"] == None
    assert data["point_herpetofauna_translocation_id"] == point_herpetofauna_translocation_id

# Test for delete translocation herpetofauna
@pytest.mark.asyncio
async def test_delete_translocation_herpetofauna(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    #create a translocation herpetofauna
    specie_id = await create_specie(async_client)
    transect_herpetofauna_translocation_id : int = await create_transect_herpetofauna_translocation(async_client)
    mark_herpetofauna_id: int = await create_mark_herpetofauna(async_client)
    code = random_string()

    response: Response = await async_client.post(
        "/api/translocation_herpetofauna", json={
            "cod": code,
            "transect_herpetofauna_translocation_id": transect_herpetofauna_translocation_id,
            "point_herpetofauna_translocation_id": None,
            "specie_id": specie_id,
            "mark_herpetofauna_id": mark_herpetofauna_id,
        },
    )
    assert response.status_code == 201
    data = response.json()
    translocation_herpetofauna_id = data["id"]

    #delete translocation herpetofauna
    response: Response = await async_client.delete(
        f"/api/translocation_herpetofauna/{translocation_herpetofauna_id}",
    )
    data = response.json()
    assert response.status_code == 200
    assert data['detail'] == "Translocation herpetofauna deleted successfully"

