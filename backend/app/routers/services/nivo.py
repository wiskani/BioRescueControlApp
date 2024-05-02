from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.nivo.utils import (
        get_flora_families_rescues,
        get_flora_families_relocation,
        get_herpetofauna_families_rescues,
        get_mammals_families_rescues,
        )
from app.services.nivo.sunburst import create_sunburst_data

from app.services.nivo.barchart import create_barchart_family

from app.api.deps import PermissonsChecker, get_db

from app.schemas.nivo import (
        SunburstBase,
        BarChartFamily
        )

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
    flora_families = await get_flora_families_rescues(db)
    herpetofauna_families = await get_herpetofauna_families_rescues(db)
    mammals_families = await get_mammals_families_rescues(db)

    # create sunburst data
    sunburst_data = create_sunburst_data(
            flora_families,
            herpetofauna_families,
            mammals_families,
            )

    return sunburst_data


# Get Bar Chart data for all rescues
@router.get(
        path="/api/nivo/barchart/flora",
        response_model=List[BarChartFamily],
        tags=["nivo"],
        status_code=status.HTTP_200_OK,
        summary="Get Bar Chart data for all rescues of flora",
        )
async def get_barchart_data_flora(
        db: AsyncSession = Depends(get_db),
        authorized: bool = Depends(PermissonsChecker(["admin"])),
        ) -> List[BarChartFamily]:
    # get list of families
    flora_families_rescues = await get_flora_families_rescues(db)
    flora_families_relocation = await get_flora_families_relocation(db)

    # create bar chart data
    bar_chart_data = create_barchart_family(
            flora_families_rescues,
            flora_families_relocation,
            )

    return bar_chart_data
