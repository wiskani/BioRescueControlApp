from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.nivo import (
        SunburstBase
        )


#generate a sunburst data structure
async def generate_sunburst_data(db:AsyncSession):


