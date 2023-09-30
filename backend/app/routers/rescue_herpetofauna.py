from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Union, Dict

from app.schemas.rescue_herpetofauna import (
    # AgeGroup
    AgeGroupBase,
    AgeGroupCreate,
    AgeGroupResponse,

    # RescueHerpetofauna
    RescueHerpetofaunaBase,
    RescueHerpetofaunaCreate,
    RescueHerpetofaunaResponse
)

from app.models.rescue_herpetofauna import AgeGroup, RescueHerpetofauna

from app.crud.rescue_herpetofauna import (
    # AgeGroup
    get_age_group_name,
    get_age_group_by_id,
    get_all_age_groups,
    create_age_group,
    update_age_group,
    delete_age_group,

    # RescueHerpetofauna
    get_rescue_herpetofauna_by_id,
    get_all_rescue_herpetofauna,
    create_rescue_herpetofauna,
    update_rescue_herpetofauna,
    delete_rescue_herpetofauna
)


