from requests import Response
from typing import Dict, Any, Union
from fastapi.testclient import TestClient

from app.tests.conftest import *
from app.tests.utils.users import *
from app.tests.utils.species_example import *


"""TESTS FOR CLASSES"""
#test create class
def test_create_class() -> None:
    name_class = random_string()
    global class_id

    response = client.post(
        "/api/classes/", json={
            "class_name": name_class,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    assert data["class_name"] == name_class
    assert "id" in data
    class_id = data["id"]

#test create class with invalid name
def test_create_class_invalid_name() -> None:
    name_class = random_string()

    response = client.post(
        "/api/classes/", json={
            "class_name": name_class,
        },
    )
    response = client.post(
        "/api/classes/", json={
            "class_name": name_class,
        },
    )
    assert response.status_code == 409, response.text

#test update class
def test_update_class() -> None:
    name_class = random_string()

    response = client.post(
        "/api/classes/", json={
            "class_name": name_class,
        },
    )

    data: Dict[str, Any] = response.json()
    id = data["id"]

    name_class = random_string()

    response = client.put(
        f"/api/classes/{id}", json={
            "class_name": name_class,
        },
    )
    assert response.status_code == 200, response.text

#test get all classes
def test_get_all_classes() -> None:
    name_class = random_string()
    name_class2 = random_string()

    response = client.post(
        "/api/classes/", json={
            "class_name": name_class,
        },
    )

    response = client.post(
        "/api/classes/", json={
            "class_name": name_class2,
        },
    )

    response = client.get(
        "/api/classes/",
    )
    assert response.status_code == 200, response.text
    data: Dict[str, Any] = response.json()
    assert len(data) > 2

#test get class by id
def test_get_class_by_id() -> None:
    name_class = random_string()

    response = client.post(
        "/api/classes/", json={
            "class_name": name_class,
        },
    )

    data = response.json()
    id = data["id"]

    response = client.get(
        f"/api/classes/{id}",
    )
    assert response.status_code == 200, response.text

#test delete class
def test_delete_class() -> None:
    name_class = random_string()

    response = client.post(
        "/api/classes/", json={
            "class_name": name_class,
        },
    )

    data = response.json()
    id = data["id"]

    response = client.delete(
        f"/api/classes/{id}",
    )
    assert response.status_code == 200, response.text

"""Test for orders"""
#test create order
def test_create_order() -> None:
    name_order = random_string()
    global order_id

    response = client.post(
        "/api/orders/", json={
            "order_name": name_order,
            "class__id": class_id,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    assert data["order_name"] == name_order
    assert "id" in data
    order_id = data["id"]

#test create order with invalid name
def test_create_order_invalid_name() -> None:
    name_order = random_string()

    response = client.post(
        "/api/orders/", json={
            "order_name": name_order,
            "class__id": class_id,
        },
    )
    response = client.post(
        "/api/orders/", json={
            "order_name": name_order,
            "class__id": class_id,
        },
    )
    assert response.status_code == 409, response.text

#test update order
def test_update_order() -> None:
    name_order = random_string()

    response = client.post(
        "/api/orders/", json={
            "order_name": name_order,
            "class__id": class_id,
        },
    )

    data: Dict[str, Any] = response.json()
    id = data["id"]

    name_order = random_string()

    response = client.put(
        f"/api/orders/{id}", json={
            "order_name": name_order,
            "class__id": class_id,
        },
    )
    assert response.status_code == 200, response.text

#test get all orders
def test_get_all_orders() -> None:
    name_order = random_string()

    name_order2 = random_string()

    response = client.post(
        "/api/orders/", json={
            "order_name": name_order,
            "class__id": class_id,
        },
    )

    response = client.post(
        "/api/orders/", json={
            "order_name": name_order2,
            "class__id": class_id,
        },
    )

    response = client.get(
        "/api/orders/",
    )
    assert response.status_code == 200, response.text
    data: Dict[str, Any] = response.json()
    assert len(data) > 2

#test get order by id
def test_get_order_by_id() -> None:
    name_order = random_string()

    response = client.post(
        "/api/orders/", json={
            "order_name": name_order,
            "class__id": class_id,
        },
    )

    data = response.json()
    id = data["id"]

    response = client.get(
        f"/api/orders/{id}",
    )
    assert response.status_code == 200, response.text

#test delete order
def test_delete_order() -> None:
    name_order = random_string()

    response = client.post(
        "/api/orders/", json={
            "order_name": name_order,
            "class__id": class_id,
        },
    )

    data = response.json()
    id = data["id"]

    response = client.delete(
        f"/api/orders/{id}",
    )
    assert response.status_code == 200, response.text

"""TESTS FOR FAMILY"""""
#test create family
def test_create_family() -> None:
    name_family = random_string()
    global family_id

    response = client.post(
        "/api/families/", json={
            "family_name": name_family,
            "order_id": order_id,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    assert data["family_name"] == name_family
    assert "id" in data
    family_id = data["id"]

#test create family with invalid name
def test_create_family_invalid_name() -> None:
    name_family = random_string()

    response = client.post(
        "/api/families/", json={
            "family_name": name_family,
            "order_id": order_id,
        },
    )
    response = client.post(
        "/api/families/", json={
            "family_name": name_family,
            "order_id": order_id,
        },
    )
    assert response.status_code == 409, response.text

#test update family
def test_update_family() -> None:
    name_family = random_string()

    response = client.post(
        "/api/families/", json={
            "family_name": name_family,
            "order_id": order_id,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    assert data["family_name"] == name_family

    name_family = random_string()

    response = client.put(
        f"/api/families/{data['id']}", json={
            "family_name": name_family,
            "order_id": order_id,
        },
    )
    assert response.status_code == 200, response.text
    data: Dict[str, Any] = response.json()
    assert data["family_name"] == name_family

#test get all families
def test_get_all_families() -> None:
    name_family = random_string()

    name_family2 = random_string()

    response = client.post(
        "/api/families/", json={
            "family_name": name_family,
            "order_id": order_id,
        },
    )

    response = client.post(
        "/api/families/", json={
            "family_name": name_family2,
            "order_id": order_id,
        },
    )

    response = client.get(
        "/api/families/",
    )
    assert response.status_code == 200, response.text
    data: Dict[str, Any] = response.json()
    assert len(data) > 2

#test get family by id
def test_get_family_by_id() -> None:
    name_family = random_string()

    response = client.post(
        "/api/families/", json={
            "family_name": name_family,
            "order_id": order_id,
        },
    )

    data = response.json()
    id = data["id"]

    response = client.get(
        f"/api/families/{id}",
    )
    assert response.status_code == 200, response.text

    #test delete family
def test_delete_family() -> None:
    name_family = random_string()

    response = client.post(
        "/api/families/", json={
            "family_name": name_family,
            "order_id": order_id,
        },
    )

    data = response.json()
    id = data["id"]

    response = client.delete(
        f"/api/families/{id}",
    )
    assert response.status_code == 200, response.text

"""TESTS FOR GENUS"""
#test create genus
def test_create_genus() -> None:
    name_genus = random_string()
    global genus_id

    response = client.post(
        "/api/genuses/", json={
            "genus_name": name_genus,
            "family_id": family_id,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    assert data["genus_name"] == name_genus
    assert "id" in data
    genus_id = data["id"]

#test create genus with invalid name
def test_create_genus_invalid_name() -> None:
    name_genus = random_string()

    response = client.post(
        "/api/genuses/", json={
            "genus_name": name_genus,
            "family_id": family_id,
        },
    )
    response = client.post(
        "/api/genuses/", json={
            "genus_name": name_genus,
            "family_id": family_id,
        },
    )
    assert response.status_code == 409, response.text

#test update genus
def test_update_genus() -> None:
    name_genus = random_string()

    response = client.post(
        "/api/genuses/", json={
            "genus_name": name_genus,
            "family_id": family_id,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    assert data["genus_name"] == name_genus

    name_genus = random_string()

    response = client.put(
        f"/api/genuses/{data['id']}", json={
            "genus_name": name_genus,
            "family_id": family_id,
        },
    )
    assert response.status_code == 200, response.text
    data: Dict[str, Any] = response.json()
    assert data["genus_name"] == name_genus

#test get all genuses
def test_get_all_genuses() -> None:
    name_genus = random_string()

    name_genus2 = random_string()

    response = client.post(
        "/api/genuses/", json={
            "genus_name": name_genus,
            "family_id": family_id,
        },
    )

    response = client.post(
        "/api/genuses/", json={
            "genus_name": name_genus2,
            "family_id": family_id,
        },
    )

    response = client.get(
        "/api/genuses/",
    )
    assert response.status_code == 200, response.text
    data: Dict[str, Any] = response.json()
    assert len(data) > 2

#test get genus by id
def test_get_genus_by_id() -> None:
    name_genus = random_string()

    response = client.post(
        "/api/genuses/", json={
            "genus_name": name_genus,
            "family_id": family_id,
        },
    )

    data = response.json()
    id = data["id"]

    response = client.get(
        f"/api/genuses/{id}",
    )
    assert response.status_code == 200, response.text


"""TESTS FOR SPECIES"""""
#test species creation
def test_create_species() -> int :
    name_scientific = random_string()
    name_common = random_string()

    response = client.post(
        "/api/species/", json={
            "scientific_name": name_scientific,
            "common_name": name_common,
            "genus_id": genus_id,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    assert data["scientific_name"] == name_scientific
    assert data["common_name"] == name_common
    assert "id" in data
    return data["id"]


#test species creation with invalid name
def test_create_species_invalid_name() -> None:
    name_scientific = random_string()
    name_common = random_string()

    response = client.post(
        "/api/species/", json={
            "scientific_name": name_scientific,
            "common_name": name_common,
            "genus_id": genus_id,
        },
    )
    response = client.post(
        "/api/species/", json={
            "scientific_name": name_scientific,
            "common_name": name_common,
            "genus_id": genus_id,
        },
    )
    assert response.status_code == 409, response.text

#test update species
def test_update_species() -> None:
    name_scientific = random_string()
    name_common = random_string()

    response = client.post(
        "/api/species/", json={
            "scientific_name": name_scientific,
            "common_name": name_common,
            "genus_id": genus_id,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    assert data["scientific_name"] == name_scientific
    assert data["common_name"] == name_common

    name_scientific = random_string()
    name_common = random_string()

    response = client.put(
        f"/api/species/{data['id']}", json={
            "scientific_name": name_scientific,
            "common_name": name_common,
            "genus_id": genus_id,
        },
    )
    assert response.status_code == 200, response.text
    data: Dict[str, Any] = response.json()
    assert data["scientific_name"] == name_scientific
    assert data["common_name"] == name_common

#test get all species
def test_get_all_species() -> None:
    name_scientific = random_string()
    name_common = random_string()

    name_scientific2 = random_string()
    name_common2 = random_string()

    response = client.post(
        "/api/species/", json={
            "scientific_name": name_scientific,
            "common_name": name_common,
            "genus_id": genus_id,
        },
    )

    response = client.post(
        "/api/species/", json={
            "scientific_name": name_scientific2,
            "common_name": name_common2,
            "genus_id": genus_id,
        },
    )

    response = client.get(
        "/api/species/",
    )
    assert response.status_code == 200, response.text
    data: Dict[str, Any] = response.json()
    assert len(data) > 2

#test get species by id
def test_get_species_by_id() -> None:
    name_scientific = random_string()
    name_common = random_string()

    response = client.post(
        "/api/species/", json={
            "scientific_name": name_scientific,
            "common_name": name_common,
            "genus_id": genus_id,
        },
    )

    data = response.json()
    id = data["id"]

    response = client.get(
        f"/api/species/{id}",
    )
    assert response.status_code == 200, response.text

