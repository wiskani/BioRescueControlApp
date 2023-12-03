from httpx import Response, AsyncClient
from typing import Dict, Any, Union
import pytest

from app.tests.conftest import *
from app.tests.utils.species_example import *
from app.tests.utils.rescue_mammals import *
from app.tests.utils.rescue_herpetofauna import *
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
    assert response.status_code == 200
    assert data["detail"] == "Habitat deleted successfully"

"""
TEST RESCUE MAMMALS
"""

#test create rescue mammal
@pytest.mark.asyncio
async def test_create_rescue_mammal(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    habitat_id = await create_habitat(async_client)
    age_group_id = await create_age_group(async_client)
    specie_id = await create_specie(async_client)
    genus_id = await create_genus(async_client)
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
    assert data["cod"] == cod
    assert data["date"] == "2021-10-10T00:00:00Z"
    assert data["mark"] == "mark"
    assert data["longitude"] == 1.0
    assert data["latitude"] == 1.0
    assert data["altitude"] == 10
    assert data["gender"] == True
    assert data["LT"] == 1.0
    assert data["LC"] == 1.0
    assert data["LP"] == 1.0
    assert data["LO"] == 1.0
    assert data["LA"] == 1.0
    assert data["weight"] == 10
    assert data["observation"] == "observation"
    assert data["is_specie_confirmed"] == True
    assert data["habitat_id"] == habitat_id
    assert data["age_group_id"] == age_group_id
    assert data["specie_id"] == specie_id

#test create rescue mammal with specie and genus 
@pytest.mark.asyncio
async def test_create_rescue_mammal_with_specie_and_genus(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    habitat_id = await create_habitat(async_client)
    age_group_id = await create_age_group(async_client)
    specie_id = await create_specie(async_client)
    genus_id = await create_genus(async_client)
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
            "genus_id": genus_id
        },
    )
    data = response.json()
    assert response.status_code == 400
    assert data["detail"] == "if specie exists, genus must be null"

#test create rescue mammal with specie and genus are null same time
@pytest.mark.asyncio
async def test_create_rescue_mammal_with_specie_and_genus_are_null_same_time(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    habitat_id = await create_habitat(async_client)
    age_group_id = await create_age_group(async_client)
    specie_id = await create_specie(async_client)
    genus_id = await create_genus(async_client)
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
            "specie_id": None,
            "genus_id": None
        },
    )
    data = response.json()
    assert response.status_code == 400
    assert data["detail"] == "specie or genus must be not null"




#test for create rescue mammal with cod already exists
@pytest.mark.asyncio
async def test_create_rescue_mammal_cod_already_exists(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    habitat_id = await create_habitat(async_client)
    age_group_id = await create_age_group(async_client)
    specie_id = await create_specie(async_client)
    genus_id = await create_genus(async_client)
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
            "specie_id": None,
            "genus_id": genus_id
        },
    )
    data = response.json()
    assert response.status_code == 201

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
            "specie_id": None,
            "genus_id": genus_id
        },
    )
    data = response.json()
    assert response.status_code == 409
    assert data["detail"] == "Rescue mammal already exists"

#test for get all rescue mammals
@pytest.mark.asyncio
async def test_get_all_rescue_mammals(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    #create two rescue mammals
    habitat_id = await create_habitat(async_client)
    age_group_id = await create_age_group(async_client)
    specie_id = await create_specie(async_client)
    cod1 = random_string()
    cod2 = random_string()

    response = await async_client.post(
        "api/rescue_mammals", json={
            "cod": cod1,
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
    assert response.status_code == 201

    response = await async_client.post(
        "api/rescue_mammals", json={
            "cod": cod2,
            "date": "2021-10-10T00:00:00",
            "mark": "mark2",
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
    print(f"La respuesta es {data}")
    assert response.status_code == 201

    response = await async_client.get("api/rescue_mammals")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2

#test for get rescue mammal by id
@pytest.mark.asyncio
async def test_get_rescue_mammal_by_id(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    #create rescue mammal
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
    assert data["cod"] == cod
    assert data["mark"] == "mark"
    assert data["longitude"] == 1.0
    assert data["latitude"] == 1.0
    assert data["altitude"] == 10
    assert data["gender"] == True
    assert data["LT"] == 1.0
    assert data["LC"] == 1.0
    assert data["LP"] == 1.0
    assert data["LO"] == 1.0
    assert data["LA"] == 1.0
    assert data["weight"] == 10
    assert data["observation"] == "observation"
    assert data["is_specie_confirmed"] == True
    assert data["habitat_id"] == habitat_id
    assert data["age_group_id"] == age_group_id
    assert data["specie_id"] == specie_id
    assert data["genus_id"] == None

#test for get rescue mammal by id not found
@pytest.mark.asyncio
async def test_get_rescue_mammal_by_id_not_found(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    response = await async_client.get("api/rescue_mammals/1")
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Rescue Mammals not found"

#test for update rescue mammal
@pytest.mark.asyncio
async def test_update_rescue_mammal(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    #create rescue mammal
    habitat_id = await create_habitat(async_client)
    age_group_id = await create_age_group(async_client)
    specie_id = await create_specie(async_client)
    genus_id = await create_genus(async_client)
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

    response = await async_client.put(
        f"api/rescue_mammals/{data['id']}", json={
            "cod": cod,
            "date": "2022-10-10T00:00:00",
            "mark": "mark2",
            "longitude": 3.0,
            "latitude": 3.0,
            "altitude": 13,
            "gender": False,
            "LT": 3.0,
            "LC": 3.0,
            "LP": 3.0,
            "LO": 3.0,
            "LA": 3.0,
            "weight": 13,
            "observation": "observation2",
            "is_specie_confirmed": False,
            "habitat_id": habitat_id,
            "age_group_id": age_group_id,
            "specie_id": None,
            "genus_id": genus_id
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data["cod"] == cod
    assert data["mark"] == "mark2"
    assert data["longitude"] == 3.0
    assert data["latitude"] == 3.0
    assert data["altitude"] == 13
    assert data["gender"] == False
    assert data["LT"] == 3.0
    assert data["LC"] == 3.0
    assert data["LP"] == 3.0
    assert data["LO"] == 3.0
    assert data["LA"] == 3.0
    assert data["weight"] == 13
    assert data["observation"] == "observation2"
    assert data["is_specie_confirmed"] == False
    assert data["habitat_id"] == habitat_id
    assert data["age_group_id"] == age_group_id
    assert data["specie_id"] == None
    assert data["genus_id"] == genus_id

#test for delete rescue mammal
@pytest.mark.asyncio
async def test_delete_rescue_mammal(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    #create rescue mammal
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

    #delete rescue mammal
    response = await async_client.delete(f"api/rescue_mammals/{data['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["detail"] == "Rescue Mammals deleted successfully"

#test for delete rescue mammal not found
@pytest.mark.asyncio
async def test_delete_rescue_mammal_not_found(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    response = await async_client.delete("api/rescue_mammals/1")
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Rescue Mammals not found"

"""
TEST FOR SITE RELEASE MAMMALS
"""

#test for create site release mammal
@pytest.mark.asyncio
async def test_create_site_release_mammal(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name = random_string()

    response = await async_client.post(
        "api/site_release_mammals", json={
            "name": name,
        }
    )
    data = response.json()
    assert response.status_code == 201
    assert data["name"] == name

#test for get all site release mammals
@pytest.mark.asyncio
async def test_get_all_site_release_mammals(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    #create two site release mammals
    name1 = random_string()
    name2 = random_string()

    response = await async_client.post(
        "api/site_release_mammals", json={
            "name": name1,
        }
    )
    assert response.status_code == 201

    response = await async_client.post(
        "api/site_release_mammals", json={
            "name": name2,
        }
    )
    assert response.status_code == 201

    #get all site release mammals
    response = await async_client.get("api/site_release_mammals")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["name"] == name1
    assert data[1]["name"] == name2

#test for get site release mammal by id
@pytest.mark.asyncio
async def test_get_site_release_mammal_by_id(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    #create site release mammal
    name = random_string()

    response = await async_client.post(
        "api/site_release_mammals", json={
            "name": name,
        }
    )
    data = response.json()
    assert response.status_code == 201

    #get site release mammal by id
    response = await async_client.get(f"api/site_release_mammals/{data['id']}")
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == name

#test for get site release mammal by id not found
@pytest.mark.asyncio
async def test_get_site_release_mammal_by_id_not_found(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    response = await async_client.get("api/site_release_mammals/1")
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Site Release Mammals not found"

#test for update site release mammal
@pytest.mark.asyncio
async def test_update_site_release_mammal(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    #create site release mammal
    name = random_string()

    response = await async_client.post(
        "api/site_release_mammals", json={
            "name": name,
        }
    )
    data = response.json()
    assert response.status_code == 201

    #update site release mammal
    response = await async_client.put(
        f"api/site_release_mammals/{data['id']}", json={
            "name": "name2",
        }
    )
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "name2"

#test for update site release mammal not found
@pytest.mark.asyncio
async def test_update_site_release_mammal_not_found(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    response = await async_client.put(
        "api/site_release_mammals/1", json={
            "name": "name2",
        }
    )
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Site Release Mammal not found"

#test for delete site release mammal
@pytest.mark.asyncio
async def test_delete_site_release_mammal(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    #create site release mammal
    name = random_string()

    response = await async_client.post(
        "api/site_release_mammals", json={
            "name": name,
        }
    )
    data = response.json()
    assert response.status_code == 201

    #delete site release mammal
    response = await async_client.delete(f"api/site_release_mammals/{data['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["detail"] == "Site Release Mammals deleted successfully"

"""
TEST FOR RELEASE MAMMALS
"""
#test for create release mammal
@pytest.mark.asyncio
async def test_create_release_mammal(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    cod = random_string()
    site_release_mammals_id: int = await create_site_release(async_client)
    rescue_mammals_id: int = await create_rescue_mammals(async_client)

    response = await async_client.post(
        "api/release_mammals", json={
            "cod": cod,
            "longitude": 1.0,
            "latitude": 1.0,
            "altitude": 10,
            "sustrate": "substrate",
            "site_release_mammals_id": site_release_mammals_id,
            "rescue_mammals_id": rescue_mammals_id,
        }
    )
    data = response.json()
    print(f"La respuesta es: {data}")
    assert response.status_code == 201
    assert data["cod"] == cod

#test for get all release mammals
@pytest.mark.asyncio
async def test_get_all_release_mammals(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    #create two release mammals
    cod1 = random_string()
    cod2 = random_string()
    site_release_mammals_id: int = await create_site_release(async_client)
    rescue_mammals_id: int = await create_rescue_mammals(async_client)

    response = await async_client.post(
        "api/release_mammals", json={
            "cod": cod1,
            "longitude": 1.0,
            "latitude": 1.0,
            "altitude": 10,
            "sustrate": "substrate",
            "site_release_mammals_id": site_release_mammals_id,
            "rescue_mammals_id": rescue_mammals_id,
        }
    )
    assert response.status_code == 201

    response = await async_client.post(
        "api/release_mammals", json={
            "cod": cod2,
            "longitude": 1.0,
            "latitude": 1.0,
            "altitude": 10,
            "sustrate": "substrate",
            "site_release_mammals_id": site_release_mammals_id,
            "rescue_mammals_id": rescue_mammals_id,
        }
    )
    assert response.status_code == 201

    #get all release mammals
    response = await async_client.get("api/release_mammals")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["cod"] == cod1
    assert data[1]["cod"] == cod2

#test for get release mammal by id
@pytest.mark.asyncio
async def test_get_release_mammal_by_id(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    #create release mammal
    cod = random_string()
    site_release_mammals_id: int = await create_site_release(async_client)
    rescue_mammals_id: int = await create_rescue_mammals(async_client)

    response = await async_client.post(
        "api/release_mammals", json={
            "cod": cod,
            "longitude": 1.0,
            "latitude": 1.0,
            "altitude": 10,
            "sustrate": "substrate",
            "site_release_mammals_id": site_release_mammals_id,
            "rescue_mammals_id": rescue_mammals_id,
        }
    )
    data = response.json()
    assert response.status_code == 201

    #get release mammal by id
    response = await async_client.get(f"api/release_mammals/{data['id']}")
    data = response.json()
    assert response.status_code == 200
    assert data["cod"] == cod

#test for get release mammal by id not found
@pytest.mark.asyncio
async def test_get_release_mammal_by_id_not_found(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    response = await async_client.get("api/release_mammals/1")
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Release Mammals not found"

#test for update release mammal
@pytest.mark.asyncio
async def test_update_release_mammal(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    #create release mammal
    cod = random_string()
    site_release_mammals_id: int = await create_site_release(async_client)
    rescue_mammals_id: int = await create_rescue_mammals(async_client)

    response = await async_client.post(
        "api/release_mammals", json={
            "cod": cod,
            "longitude": 1.0,
            "latitude": 1.0,
            "altitude": 10,
            "sustrate": "substrate",
            "site_release_mammals_id": site_release_mammals_id,
            "rescue_mammals_id": rescue_mammals_id,
        }
    )
    data = response.json()
    assert response.status_code == 201

    #update release mammal
    response = await async_client.put(
        f"api/release_mammals/{data['id']}", json={
            "cod": "cod2",
            "longitude": 2.0,
            "latitude": 2.0,
            "altitude": 20,
            "sustrate": "substrate2",
            "site_release_mammals_id": site_release_mammals_id,
            "rescue_mammals_id": rescue_mammals_id,

        }
    )
    data = response.json()
    assert response.status_code == 200
    assert data["cod"] == "cod2"
    assert data["longitude"] == 2.0
    assert data["latitude"] == 2.0
    assert data["altitude"] == 20
    assert data["sustrate"] == "substrate2"

#test for update release mammal not found
@pytest.mark.asyncio
async def test_update_release_mammal_not_found(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    response = await async_client.put(
        "api/release_mammals/1", json={
            "cod": "cod2",
            "longitude": 2.0,
            "latitude": 2.0,
            "altitude": 20,
            "sustrate": "substrate2",
            "site_release_mammals_id": 1,
            "rescue_mammals_id": 1,

        }
    )
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Release Mammal not found"

#test for delete release mammal
@pytest.mark.asyncio
async def test_delete_release_mammal(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    #create release mammal
    cod = random_string()
    site_release_mammals_id: int = await create_site_release(async_client)
    rescue_mammals_id: int = await create_rescue_mammals(async_client)

    response = await async_client.post(
        "api/release_mammals", json={
            "cod": cod,
            "longitude": 1.0,
            "latitude": 1.0,
            "altitude": 10,
            "sustrate": "substrate",
            "site_release_mammals_id": site_release_mammals_id,
            "rescue_mammals_id": rescue_mammals_id,
        }
    )
    data = response.json()
    assert response.status_code == 201

    #delete release mammal
    response = await async_client.delete(f"api/release_mammals/{data['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["detail"] == "Release Mammals deleted successfully"

"""
CRUD GET RESCUE MAMMALS WITH SPECIES AND GENUS
"""

#test for get rescue mammals with specie and genus
@pytest.mark.asyncio
async def test_get_rescue_mammals_with_specie_and_genus(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:

    rescue_mammals_id, cod, specie, genus = await create_rescue_mammalsWithCodSpecieGenus(async_client)


    response = await async_client.get(
            "/api/rescue_mammals_species",
            )

    data = response.json()
    print(f"La respuesta es: {data}")
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["cod"] == cod
    assert data[0]["specie_name"] == specie
    assert data[0]["genus_name"] == genus


























