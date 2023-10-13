from urllib import response
import pytest
import random
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from httpx import Response, AsyncClient
from app.tests.conftest import *
from app.models.towers import Tower

#Create a tower
@pytest.mark.asyncio
async def create_random_tower(
    async_client: AsyncClient,
) -> int:
    response: Response = await async_client.post(
        "/api/towers", json={
            "number": random.randint(1, 100),
            "latitude": random.uniform(-90, 90),
            "longitude": random.uniform(-180, 180),
        },
    )
    assert response.status_code == 201
    data: Dict[str, Any] = response.json()
    tower_id = data["id"]
    return tower_id
