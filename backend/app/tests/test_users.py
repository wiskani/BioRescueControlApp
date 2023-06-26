from pydantic import EmailStr
from requests import Response
from typing import Dict, Any, Union
from fastapi.testclient import TestClient

from app.tests.conftest import *
from app.tests.utils.users import *


# test for user creation
def test_create_user() -> None:
    mail: EmailStr | str = random_email_user()
    password: str = random_password()
    id_number: int = random_int_user()

    response: Response  = client.post(
        "/api/users/", json={
            "id": id_number,
            "email": mail,
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



