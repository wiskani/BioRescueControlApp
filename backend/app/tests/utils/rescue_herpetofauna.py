import random
import string
import pytest
from httpx import Response, AsyncClient
from typing import Dict, Any
from app.tests.conftest import *
#make a fuction that return a random string of 10 characters
def random_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=10))

#Create a Age Group
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
