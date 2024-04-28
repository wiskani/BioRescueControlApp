from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.nivo.sunburst import (
        create_sunburst_data,
        get_flora_families,
        get_herpetofauna_families,
        get_mammals_families,
        )

from app.api.deps import PermissonsChecker, get_db

from app.schemas.nivo import SunburstBase

router = APIRouter()


# Get Sunburst data for all rescues
@router.get(
        path="/api/nivo/sunburst",
        response_model=SunburstBase,
        tags=["nivo"],
        status_code=status.HTTP_200_OK,
        summary="Get Sunburst data for all rescues",
        )
async def get_sunburst_data(
        db: AsyncSession = Depends(get_db),
        authorized: bool = Depends(PermissonsChecker(["admin"])),
        ) -> SunburstBase:
    # get list of families
    flora_families = await get_flora_families(db)
    herpetofauna_families = await get_herpetofauna_families(db)
    mammals_families = await get_mammals_families(db)

    # create sunburst data
    sunburst_data = create_sunburst_data(
            flora_families,
            herpetofauna_families,
            mammals_families,
            )

    return sunburst_data
