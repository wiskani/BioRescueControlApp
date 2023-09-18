from pydantic import EmailStr
from httpx import Response, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, Union
import pytest

from app.tests.utils.users import *
from app.tests.conftest import async_client


# test for user creation
@pytest.mark.asyncio
async def test_create_user(
    async_client: AsyncClient,
) -> None:
    mail: Union [EmailStr , str] = random_email_user()
    name: str = random_name_user()
    last_name: str = radom_last_name()
    password: str = random_password()
    id_number: int = random_int_user()

    response: Response  = await async_client.post(
        "/api/users", json={
            "id": id_number,
            "email": mail,
            "name": name,
            "last_name": last_name,
            "permissions":["admin"],
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
@pytest.mark.asyncio
async def test_create_user_invalid_email(
    async_client: AsyncClient,
) -> None:
    mail = random_email_user()
    name: str = random_name_user()
    last_name: str = radom_last_name()
    password: str = random_password()
    id_number: int = random_int_user()
    id_number_2: int = random_int_user()

    response: Response = await async_client.post(
        "/api/users", json={
            "id": id_number,
            "email": mail,
            "name": name,
            "last_name": last_name,
            "permissions":["admin"],
            "hashed_password": password,
        },
    )
    assert response.status_code == 201, response.text
    response: Response =await async_client.post(
        "/api/users", json={
            "id": id_number_2,
            "email": mail,
            "name": name,
            "last_name": last_name,
            "permissions":["admin"],
            "hashed_password": password,
        },
    )
    assert response.status_code == 400, response.text
    data: Dict[str, Any] = response.json()
    assert data["detail"] == "Email already registered"

# test for update user
@pytest.mark.asyncio
async def test_update_user(
    async_client: AsyncClient,
) -> None:
    mail: EmailStr | str = random_email_user()
    name: str = random_name_user()
    last_name: str = radom_last_name()
    password: str = random_password()
    id_number_initial: int = random_int_user()

    response: Response = await async_client.post(
        "/api/users", json={
            "id": id_number_initial,
            "email": mail,
            "name": name,
            "last_name": last_name,
            "permissions":["admin"],
            "hashed_password": password,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    id_number: Union[int, str] = data["id"]

    mail2: EmailStr|str = random_email_user()
    password2: str = random_password()

    response: Response = await async_client.put(
        f"/api/users/{id_number}", json={
            "id": id_number,
            "email": mail2,
            "name": name,
            "last_name": last_name,
            "permissions":["user-write"],
            "hashed_password": password2,
        },
    )
    assert response.status_code == 200, response.text
    data: Dict[str, Any] = response.json()
    assert data["email"] == mail2
    assert "id" in data
    user_id: Union[int, str] = data["id"]
    assert user_id is not None
    assert data["permissions"] == ["user-write"]

    # test for update user with invalid id 
@pytest.mark.asyncio
async def test_update_user_invalid_email(
    async_client: AsyncClient,  
) -> None:
    mail: EmailStr|str = random_email_user()
    name: str = random_name_user()
    last_name: str = radom_last_name()
    password: str = random_password()
    id_number: int = random_int_user()

    response: Response = await async_client.post(
        "/api/users", json={
            "id": id_number,
            "email": mail,
            "name": name,
            "last_name": last_name,
            "permissions":["admin"],
            "hashed_password": password,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()

    id_number2: int = random_int_user()

    response: Response = await async_client.put(
        f"/api/users/{id_number2}", json={
            "id": id_number,
            "email": mail,
            "name": name,
            "last_name": last_name,
            "permissions":["user-write"],
            "hashed_password": password,
        },
    )
    assert response.status_code == 400, response.text
    data: Dict[str, Any] = response.json()
    assert data["detail"] == "Something went wrong, maybe the user does not exist."

    # test for delete user
@pytest.mark.asyncio
async def test_delete_user(
    async_client: AsyncClient,
) -> None:
    mail: EmailStr|str = random_email_user()
    name: str = random_name_user()
    last_name: str = radom_last_name()
    password: str = random_password()
    id_number_inicial: int = random_int_user()

    response: Response = await async_client.post(
        "/api/users", json={
            "id": id_number_inicial,
            "email": mail,
            "name": name,
            "last_name": last_name,
            "permissions":["admin"],
            "hashed_password": password,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()
    id_number: Union[int, str] = data["id"]

    response: Response = await async_client.delete(f"/api/users/{id_number}")
    assert response.status_code == 200, response.text

# test for delete user with invalid id
@pytest.mark.asyncio
async def test_delete_user_invalid_email(
    async_client: AsyncClient,
) -> None:
    mail: EmailStr|str = random_email_user()
    name: str = random_name_user()
    last_name: str = radom_last_name()
    password: str = random_password()
    id_number: int = random_int_user()

    response: Response = await async_client.post(
        "/api/users", json={
            "id": id_number,
            "email": mail,
            "name": name,
            "last_name": last_name,
            "permissions":["admin"],
            "hashed_password": password,
        },
    )
    assert response.status_code == 201, response.text
    data: Dict[str, Any] = response.json()

    id_number2: int = random_int_user()

    response: Response = await async_client.delete(f"/api/users/{id_number2}")
    assert response.status_code == 400, response.text
    data: Dict[str, Any] = response.json()
    assert data["detail"] == "Something went wrong, maybe the user does not exist."


