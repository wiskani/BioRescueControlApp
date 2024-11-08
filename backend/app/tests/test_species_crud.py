from httpx import Response, AsyncClient
from typing import Dict, Any, Union
import pytest

from app.tests.conftest import *
from app.tests.utils.users import *
from app.tests.utils.species_example import *
from app.tests.conftest import async_client


"""TESTS FOR CLASSES"""


# test create class
@pytest.mark.asyncio
async def test_create_class(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_class = random_string()

    response: Response = await async_client.post(
        "/api/classes", json={
            "class_name": name_class,
            "key_gbif": 10,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    assert data["class_name"] == name_class
    assert data["key_gbif"] == 10
    assert "id" in data


# test create class with invalid name
@pytest.mark.asyncio
async def test_create_class_invalid_name(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_class = random_string()

    response = await async_client.post(
        "/api/classes", json={
            "class_name": name_class,
            "key_gbif": 10,
        },
    )
    response = await async_client.post(
        "/api/classes", json={
            "class_name": name_class,
            "key_gbif": 10,
        },
    )
    assert response.status_code == 409, response.text


# test update class
@pytest.mark.asyncio
async def test_update_class(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_class = random_string()

    response: Response = await async_client.post(
        "/api/classes", json={
            "class_name": name_class,
            "key_gbif": 10,
        },
    )

    data: Dict[str, Any] = response.json()
    id = data["id"]

    name_class = random_string()

    response = await async_client.put(
        f"/api/classes/{id}", json={
            "class_name": name_class,
            "key_gbif": 10,
        },
    )
    assert response.status_code == 200, response.text


# test get all classes
@pytest.mark.asyncio
async def test_get_all_classes(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_class = random_string()
    name_class2 = random_string()

    response: Response = await async_client.post(
        "/api/classes", json={
            "class_name": name_class,
            "key_gbif": 10,
        },
    )

    response: Response = await async_client.post(
        "/api/classes", json={
            "class_name": name_class2,
            "key_gbif": 11,
        },
    )

    response: Response = await async_client.get(
        "/api/classes",
    )
    assert response.status_code == 200, response.text
    data: Dict[str, Any] = response.json()
    assert len(data) >= 2


# test get class by id
@pytest.mark.asyncio
async def test_get_class_by_id(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_class = random_string()

    response: Response = await async_client.post(
        "/api/classes", json={
            "class_name": name_class,
            "key_gbif": 10,
        },
    )

    data = response.json()
    id = data["id"]

    response = await async_client.get(
        f"/api/classes/{id}",
    )
    assert response.status_code == 200, response.text


# test delete class
@pytest.mark.asyncio
async def test_delete_class(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_class = random_string()

    response: Response = await async_client.post(
        "/api/classes", json={
            "class_name": name_class,
            "key_gbif": 10,
        },
    )

    data = response.json()
    id = data["id"]

    response = await async_client.delete(
        f"/api/classes/{id}",
    )
    assert response.status_code == 200, response.text

"""Test for orders"""


# test create order
@pytest.mark.asyncio
async def test_create_order(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_order = random_string()
    class_id = await  create_class(async_client)
    response: Response = await async_client.post(
        "/api/orders", json={
            "order_name": name_order,
            "key_gbif": 10,
            "class__id": class_id ,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    assert data["order_name"] == name_order
    assert data["key_gbif"] == 10
    assert "id" in data


# test create order with invalid name
@pytest.mark.asyncio
async def test_create_order_invalid_name(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_order = random_string()
    class_id = await  create_class(async_client)

    response: Response = await async_client.post(
        "/api/orders", json={
            "order_name": name_order,
            "key_gbif": 10,
            "class__id": class_id,
        },
    )
    response: Response = await async_client.post(
        "/api/orders", json={
            "order_name": name_order,
            "key_gbif": 10,
            "class__id": class_id,
        },
    )
    assert response.status_code == 409, response.text


# test update order
@pytest.mark.asyncio
async def test_update_order(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_order = random_string()
    class_id = await  create_class(async_client)

    response: Response = await async_client.post(
        "/api/orders", json={
            "order_name": name_order,
            "key_gbif": 10,
            "class__id": class_id,
        },
    )

    data: Dict[str, Any] = response.json()
    id = data["id"]

    name_order = random_string()

    response: Response = await async_client.put(
        f"/api/orders/{id}", json={
            "order_name": name_order,
            "key_gbif": 10,
            "class__id": class_id,
        },
    )
    assert response.status_code == 200, response.text


# test get all orders
@pytest.mark.asyncio
async def test_get_all_orders(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_order = random_string()

    name_order2 = random_string()

    class_id = await  create_class(async_client)

    response: Response = await async_client.post(
        "/api/orders", json={
            "order_name": name_order,
            "key_gbif": 10,
            "class__id": class_id,
        },
    )

    response: Response = await async_client.post(
        "/api/orders", json={
            "order_name": name_order2,
            "key_gbif": 12,
            "class__id": class_id,
        },
    )

    response: Response = await async_client.get(
        "/api/orders",
    )
    assert response.status_code == 200, response.text
    data: Dict[str, Any] = response.json()
    assert len(data) >= 2


# test get order by id
@pytest.mark.asyncio
async def test_get_order_by_id(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_order = random_string()

    class_id = await  create_class(async_client)

    response: Response = await async_client.post(
        "/api/orders", json={
            "order_name": name_order,
            "key_gbif": 10,
            "class__id": class_id,
        },
    )

    data = response.json()
    id = data["id"]

    response: Response = await async_client.get(
        f"/api/orders/{id}",
    )
    assert response.status_code == 200, response.text


# test delete order
@pytest.mark.asyncio
async def test_delete_order(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_order = random_string()

    class_id = await  create_class(async_client)

    response: Response = await async_client.post(
        "/api/orders", json={
            "order_name": name_order,
            "key_gbif": 10,
            "class__id": class_id,
        },
    )

    data = response.json()
    id = data["id"]

    response = await async_client.delete(
        f"/api/orders/{id}",
    )
    assert response.status_code == 200, response.text

"""TESTS FOR FAMILY"""""


# test create family
@pytest.mark.asyncio
async def test_create_family(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_family = random_string()
    order_id = await  create_order(async_client)

    response: Response = await async_client.post(
        "/api/families", json={
            "family_name": name_family,
            "key_gbif": 10,
            "order_id": order_id,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    assert data["family_name"] == name_family
    assert data["key_gbif"] == 10
    assert "id" in data


# test create family with invalid name
@pytest.mark.asyncio
async def test_create_family_invalid_name(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_family = random_string()
    order_id = await  create_order(async_client)

    response: Response = await async_client.post(
        "/api/families", json={
            "family_name": name_family,
            "key_gbif": 10,
            "order_id": order_id,
        },
    )
    response: Response = await async_client.post(
        "/api/families", json={
            "family_name": name_family,
            "key_gbif": 11,
            "order_id": order_id,
        },
    )
    assert response.status_code == 409, response.text


# test update family
@pytest.mark.asyncio
async def test_update_family(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_family = random_string()
    order_id = await  create_order(async_client)

    response: Response = await async_client.post(
        "/api/families", json={
            "family_name": name_family,
            "key_gbif": 10,
            "order_id": order_id,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    assert data["family_name"] == name_family
    assert data["key_gbif"] == 10

    name_family = random_string()

    response: Response = await async_client.put(
        f"/api/families/{data['id']}", json={
            "family_name": name_family,
            "key_gbif": 10,
            "order_id": order_id,
        },
    )
    assert response.status_code == 200, response.text
    data: Dict[str, Any] = response.json()
    assert data["family_name"] == name_family
    assert data["key_gbif"] == 10


# test get all families
@pytest.mark.asyncio
async def test_get_all_families(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_family = random_string()

    name_family2 = random_string()

    order_id = await  create_order(async_client)

    response: Response = await async_client.post(
        "/api/families", json={
            "family_name": name_family,
            "key_gbif": 10,
            "order_id": order_id,
        },
    )

    response: Response = await async_client.post(
        "/api/families", json={
            "family_name": name_family2,
            "key_gbif": 11,
            "order_id": order_id,
        },
    )

    response: Response = await async_client.get(
        "/api/families",
    )
    assert response.status_code == 200, response.text
    data: Dict[str, Any] = response.json()
    assert len(data) >= 2

#test get family by id
@pytest.mark.asyncio
async def test_get_family_by_id(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_family = random_string()
    order_id = await  create_order(async_client)

    response: Response = await async_client.post(
        "/api/families", json={
            "family_name": name_family,
            "key_gbif": 10,
            "order_id": order_id,
        },
    )

    data = response.json()
    id = data["id"]

    response = await async_client.get(
        f"/api/families/{id}",
    )
    assert response.status_code == 200, response.text

#test delete family
@pytest.mark.asyncio
async def test_delete_family(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_family = random_string()
    order_id = await  create_order(async_client)

    response: Response = await async_client.post(
        "/api/families", json={
            "family_name": name_family,
            "key_gbif": 10,
            "order_id": order_id,
        },
    )

    data = response.json()
    id = data["id"]

    response: Response = await async_client.delete(
        f"/api/families/{id}",
    )
    assert response.status_code == 200, response.text

"""TESTS FOR GENUS"""
#test create genus
@pytest.mark.asyncio
async def test_create_genus(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_genus = random_string()
    family_id = await  create_family(async_client)

    response: Response = await async_client.post(
        "/api/genuses", json={
            "genus_name": name_genus,
            "key_gbif": 10,
            "family_id": family_id,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    assert data["genus_name"] == name_genus
    assert data["key_gbif"] == 10
    assert "id" in data

#test create genus with invalid name
@pytest.mark.asyncio
async def test_create_genus_invalid_name(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_genus = random_string()
    family_id = await  create_family(async_client)

    response: Response = await async_client.post(
        "/api/genuses", json={
            "genus_name": name_genus,
            "key_gbif": 10,
            "family_id": family_id,
        },
    )
    response: Response = await async_client.post(
        "/api/genuses", json={
            "genus_name": name_genus,
            "key_gbif": 11,
            "family_id": family_id,
        },
    )
    assert response.status_code == 409, response.text

#test update genus
@pytest.mark.asyncio
async def test_update_genus(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_genus = random_string()
    family_id = await  create_family(async_client)

    response: Response = await async_client.post(
        "/api/genuses", json={
            "genus_name": name_genus,
            "key_gbif": 10,
            "family_id": family_id,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    assert data["genus_name"] == name_genus

    name_genus = random_string()

    response: Response = await async_client.put(
        f"/api/genuses/{data['id']}", json={
            "genus_name": name_genus,
            "key_gbif": 10,
            "family_id": family_id,
        },
    )
    assert response.status_code == 200, response.text
    data: Dict[str, Any] = response.json()
    assert data["genus_name"] == name_genus
    assert data["key_gbif"] == 10

#test get all genuses
@pytest.mark.asyncio
async def test_get_all_genuses(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_genus = random_string()

    name_genus2 = random_string()

    family_id = await  create_family(async_client)

    response: Response = await async_client.post(
        "/api/genuses", json={
            "genus_name": name_genus,
            "key_gbif": 10,
            "family_id": family_id,
        },
    )

    response: Response = await async_client.post(
        "/api/genuses", json={
            "genus_name": name_genus2,
            "key_gbif": 11,
            "family_id": family_id,
        },
    )

    response: Response = await async_client.get(
        "/api/genuses",
    )
    assert response.status_code == 200, response.text
    data: Dict[str, Any] = response.json()
    assert len(data) >= 2

#test get genus by id
@pytest.mark.asyncio
async def test_get_genus_by_id(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_genus = random_string()

    family_id = await  create_family(async_client)

    response: Response = await async_client.post(
        "/api/genuses", json={
            "genus_name": name_genus,
            "key_gbif": 10,
            "family_id": family_id,
        },
    )

    data = response.json()
    id = data["id"]

    response = await async_client.get(
        f"/api/genuses/{id}",
    )
    assert response.status_code == 200, response.text


"""TESTS FOR SPECIES"""""
#test species creation
@pytest.mark.asyncio
async def test_create_species(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> int :
    name_scientific = random_string()
    name_common = random_string()
    genus_id = await  create_genus(async_client)
    status_id = await  create_status_specie(async_client)

    response: Response = await async_client.post(
        "/api/species", json={
            "scientific_name": name_scientific,
            "specific_epithet": name_common,
            "key_gbif": 10,
            "status_id": status_id,
            "genus_id": genus_id,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    assert data["scientific_name"] == name_scientific
    assert data["specific_epithet"] == name_common
    assert data["status_id"] == status_id
    assert data["genus_id"] == genus_id
    assert data["key_gbif"] == 10
    assert "id" in data
    return data["id"]


#test species creation with invalid name
@pytest.mark.asyncio
async def test_create_species_invalid_name(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_scientific = random_string()
    name_common = random_string()
    genus_id = await  create_genus(async_client)
    status_id = await  create_status_specie(async_client)

    response: Response  = await async_client.post(
        "/api/species", json={
            "scientific_name": name_scientific,
            "specific_epithet": name_common,
            "key_gbif": 10,
            "status_id": status_id,
            "genus_id": genus_id,
        },
    )
    response: Response = await async_client.post(
        "/api/species", json={
            "scientific_name": name_scientific,
            "specific_epithet": name_common,
            "key_gbif": 11,
            "status_id": status_id,
            "genus_id": genus_id,
        },
    )
    assert response.status_code == 409, response.text

#test update species
@pytest.mark.asyncio
async def test_update_species(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_scientific = random_string()
    name_common = random_string()
    genus_id = await  create_genus(async_client)
    status_id = await  create_status_specie(async_client)

    response: Response = await async_client.post(
        "/api/species", json={
            "scientific_name": name_scientific,
            "specific_epithet": name_common,
            "key_gbif": 10,
            "status_id": status_id,
            "genus_id": genus_id,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    assert data["scientific_name"] == name_scientific
    assert data["specific_epithet"] == name_common

    name_scientific = random_string()
    name_common = random_string()

    response: Response = await async_client.put(
        f"/api/species/{data['id']}", json={
            "scientific_name": name_scientific,
            "specific_epithet": name_common,
            "key_gbif": 11,
            "status_id": status_id,
            "genus_id": genus_id,
        },
    )
    assert response.status_code == 200, response.text
    data: Dict[str, Any] = response.json()
    assert data["scientific_name"] == name_scientific
    assert data["specific_epithet"] == name_common
    assert data["key_gbif"] == 11

#test get all species
@pytest.mark.asyncio
async def test_get_all_species(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    name_scientific = random_string()
    name_common = random_string()
    status_id = await  create_status_specie(async_client)

    name_scientific2 = random_string()
    name_common2 = random_string()
    genus_id = await  create_genus(async_client)

    response: Response = await async_client.post(
        "/api/species", json={
            "scientific_name": name_scientific,
            "specific_epithet": name_common,
            "key_gbif": 10,
            "status_id": status_id,
            "genus_id": genus_id,
        },
    )

    response: Response = await async_client.post(
        "/api/species", json={
            "scientific_name": name_scientific2,
            "specific_epithet": name_common2,
            "key_gbif": 11,
            "status_id": status_id,
            "genus_id": genus_id,
        },
    )

    response: Response = await async_client.get(
        "/api/species",
    )
    assert response.status_code == 200, response.text
    data: Dict[str, Any] = response.json()
    assert len(data) >= 2

#test get species by id
@pytest.mark.asyncio
async def test_get_species_by_id(
    async_client: AsyncClient,
    async_session: AsyncSession,
) -> None:
    species_id = await  create_specie(async_client)
    response: Response = await async_client.get(
        f"/api/species/{species_id}",
    )
    assert response.status_code == 200, response.text

