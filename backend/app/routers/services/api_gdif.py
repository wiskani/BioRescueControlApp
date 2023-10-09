from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Union, Dict, Optional

from app.services.gbif.api_gbif import get_species_suggestions, get_species_details
from app.api.deps import PermissonsChecker, get_db

from app.crud.species import (
    create_class,
    create_order,
    create_family,
    create_genus,
    create_specie
)

from app.schemas.species import SpeciesResponse


router:APIRouter = APIRouter()

"""
ENDPOINTS FOR GBIF API
"""

# Get species suggestions
@router.get(
    path="/species_gbif/suggestions",
    tags=["GBIF"],
    response_model=List[Dict],
    status_code=status.HTTP_200_OK
)
async def get_species_suggestions_endpoint(
    q: str,
    r: Optional[str] = None,
    autorized: bool = Depends(PermissonsChecker(["admin"])),
)->Dict:
    """
    Get species suggestions from GBIF API
    """
    return get_species_suggestions(q, r)

# Get species details
@router.get(
    path="/species_gbif/details",
    tags=["GBIF"],
    response_model=Dict,
    status_code=status.HTTP_200_OK
)
async def get_species_details_endpoint(
    key: str,
    autorized: bool = Depends(PermissonsChecker(["admin"])),
)->Dict:
    """
    Get species details from GBIF API
    """
    return get_species_details(key)

#createa new specie by key of gbif
@router.post(
    path="/species_gdif/create",
    tags=["GBIF"],
    response_model= SpeciesResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_specie_by_key(
    key: str,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"])),
)->SpeciesResponse:
    """
    Create a new specie by key of gbif
    """
    data : Dict = get_species_details(key)




