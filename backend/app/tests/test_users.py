from pydantic import EmailStr
from requests import Response
from typing import Dict, Any, Union
from fastapi.testclient import TestClient

from app.tests.conftest import *
from app.tests.utils.users import *


# test for user creation
def test_create_user() -> None:
    mail: Union [EmailStr , str] = random_email_user()
    name: str = random_name_user()
    last_name: str = radom_last_name()
    password: str = random_password()
    id_number: int = random_int_user()

    response: Response  = client.post(
        "/api/users/", json={
            "id": id_number,
            "email": mail,
            "name": name,
            "last_name": last_name,
            "permissions":"admin",
            "hashed_password": password,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    assert data["email"] == mail
    assert "id" in data
    assert "hashed_password" not in data
    user_id: Union[int, str] = data["id"]
    assert user_id is not None

# test for user creation with invalid email
def test_create_user_invalid_email() -> None:
    mail: EmailStr = random_email_user()
    name: str = random_name_user()
    last_name: str = radom_last_name()
    password: str = random_password()
    id_number: int = random_int_user()
    id_number_2: int = random_int_user()

    response: Response = client.post(
        "/api/users/", json={
            "id": id_number,
            "email": mail,
            "name": name,
            "last_name": last_name,
            "permissions":"admin",
            "hashed_password": password,
        },
    )
    response: Response = client.post(
        "/api/users/", json={
            "id": id_number_2,
            "email": mail,
            "name": name,
            "last_name": last_name,
            "permissions":"admin",
            "hashed_password": password,
        },
    )
    assert response.status_code == 400, response.text
    data: Dict[str, Any] = response.json()
    assert data["detail"] == "Email already registered"

# test for update user
def test_update_user() -> None:
    mail: EmailStr = random_email_user()
    name: str = random_name_user()
    last_name: str = radom_last_name()
    password: str = random_password()
    id_number: int = random_int_user()

    response: Response = client.post(
        "/api/users/", json={
            "id": id_number,
            "email": mail,
            "name": name,
            "last_name": last_name,
            "permissions":"admin",
            "hashed_password": password,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    id_number: Union[int, str] = data["id"]

    mail2: EmailStr = random_email_user()
    password2: str = random_password()

    response: Response = client.put(
        f"/api/users/{id_number}", json={
            "id": id_number,
            "email": mail2,
            "name": name,
            "last_name": last_name,
            "permissions":"user-write",
            "hashed_password": password2,
        },
    )
    assert response.status_code == 200, response.text
    data: Dict[str, Any] = response.json()
    assert data["email"] == mail2
    assert "id" in data
    user_id: Union[int, str] = data["id"]
    assert user_id is not None      
    assert data["permissions"] == "user-write"

    # test for update user with invalid id 
def test_update_user_invalid_email() -> None:
    mail: EmailStr = random_email_user()
    name: str = random_name_user()
    last_name: str = radom_last_name()
    password: str = random_password()
    id_number: int = random_int_user()

    response: Response = client.post(
        "/api/users/", json={
            "id": id_number,
            "email": mail,
            "name": name,
            "last_name": last_name,
            "permissions":"admin",
            "hashed_password": password,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()

    id_number2: int = random_int_user()

    response: Response = client.put(
        f"/api/users/{id_number2}", json={
            "id": id_number,
            "email": mail,
            "name": name,
            "last_name": last_name,
            "permissions":"user-write",
            "hashed_password": password,
        },
    )
    assert response.status_code == 400, response.text
    data: Dict[str, Any] = response.json()
    assert data["detail"] == "Something went wrong, maybe the user does not exist."

    # test for delete user
def test_delete_user() -> None:
    mail: EmailStr = random_email_user()
    name: str = random_name_user()
    last_name: str = radom_last_name()
    password: str = random_password()
    id_number: int = random_int_user()

    response: Response = client.post(
        "/api/users/", json={
            "id": id_number,
            "email": mail,
            "name": name,
            "last_name": last_name,
            "permissions":"admin",
            "hashed_password": password,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    id_number: Union[int, str] = data["id"]

    response: Response = client.delete(f"/api/users/{id_number}")
    assert response.status_code == 200, response.text

# test for delete user with invalid id
def test_delete_user_invalid_email() -> None:
    mail: EmailStr = random_email_user()
    name: str = random_name_user()
    last_name: str = radom_last_name()
    password: str = random_password()
    id_number: int = random_int_user()

    response: Response = client.post(
        "/api/users/", json={
            "id": id_number,
            "email": mail,
            "name": name,
            "last_name": last_name,
            "permissions":"admin",
            "hashed_password": password,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()

    id_number2: int = random_int_user()

    response: Response = client.delete(f"/api/users/{id_number2}")
    assert response.status_code == 400, response.text
    data: Dict[str, Any] = response.json()
    assert data["detail"] == "Something went wrong, maybe the user does not exist."




