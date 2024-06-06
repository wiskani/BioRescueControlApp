from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Union, Dict, Optional

from app.services.gbif.api_gbif import (
        get_species_suggestions,
        get_species_details,
        get_genus_details,
        get_family_details,
        )

from app.api.deps import PermissonsChecker, get_db

from app.crud.species import (
    create_class,
    get_class_by_name,
    create_order,
    get_order_by_name,
    create_family,
    get_family_by_name,
    create_genus,
    get_genus_by_name,
    create_specie,
    get_specie_by_name,
)

from app.schemas.species import (
    SpeciesResponse,
    SpeciesCreate,

    GenusesCreate,
    GenusesResponse,

    FamiliesCreate,
    FamiliesResponse,

    OrdersCreate,

    ClassesCreate,
)

from app.schemas.services import (
        SpecieGbif,
        )


from app.models.species import Specie, Genus, Family

router: APIRouter = APIRouter()

"""
ENDPOINTS FOR GBIF API
"""


# Get species suggestions
@router.get(
    path="/api/species_gbif/suggestions",
    tags=["GBIF"],
    response_model=List[Dict],
    status_code=status.HTTP_200_OK
)
async def get_species_suggestions_endpoint(
    q: str,
    r: Optional[str] = None,
    autorized: bool = Depends(PermissonsChecker(["admin"])),
) -> Dict:
    """
    Get species suggestions from GBIF API
    """
    return get_species_suggestions(q, r)


# Get species details
@router.get(
    path="/api/species_gbif/details",
    tags=["GBIF"],
    response_model=Dict,
    status_code=status.HTTP_200_OK
)
async def get_species_details_endpoint(
    key: str,
    autorized: bool = Depends(PermissonsChecker(["admin"])),
) -> SpecieGbif | HTTPException:
    """
    Get species details from GBIF API
    """
    return get_species_details(key)


# createa new specie by key of gbif
@router.post(
    path="/api/species_gdif/create",
    tags=["GBIF"],
    response_model=SpeciesResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_specie_by_key(
    key: str,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"])),
) -> Specie:
    """
    Create a new specie by key of gbif
    """
    data = get_species_details(key)
    if data is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Specie not found"
                )

    # check if class exists
    db_class = await get_class_by_name(db, data.class_)
    if db_class is None:
        new_class = ClassesCreate(
                class_name=data.class_,
                key_gbif=data.classKey
                )
        db_class = await create_class(db, new_class)

    # check if order exists
    db_order = await get_order_by_name(db, data.order)
    if db_order is None:
        new_order = OrdersCreate(
                order_name=data.order,
                key_gbif=data.orderKey,
                class__id=db_class.id
                )
        db_order = await create_order(db, new_order)

    # check if family exists
    db_family = await get_family_by_name(db, data.family)
    if db_family is None:
        new_family = FamiliesCreate(
                family_name=data.family,
                key_gbif=data.familyKey,
                order_id=db_order.id
                )
        db_family = await create_family(db, new_family)

    # check if genus exists
    db_genus = await get_genus_by_name(db, data.genus)
    if db_genus is None:
        new_genus = GenusesCreate(
                genus_name=data.genus,
                key_gbif=data.genusKey,
                family_id=db_family.id
                )
        db_genus = await create_genus(db, new_genus)

    # check if specie exists
    db_specie = await get_specie_by_name(db, data.scientificName)
    if db_specie is None:
        new_specie = SpeciesCreate(
                scientific_name=data.scientificName,
                specific_epithet=data.canonicalName,
                status_id=None,
                key_gbif=data.speciesKey,
                genus_id=db_genus.id
                )
        db_specie = await create_specie(db, new_specie)
        return db_specie

    return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Specie already exists"
            )


# create new genus  by key of gbif
@router.post(
    path="/api/genus_gdif/create",
    tags=["GBIF"],
    response_model=GenusesResponse,
    status_code=status.HTTP_201_CREATED
    )
async def create_genus_by_key(
    key: str,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"])),
) -> Genus:
    """
    Create a new genus by key of gbif
    """
    data = get_genus_details(key)
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genus not found")

    #check if class exists
    db_class = await get_class_by_name(db, data.class_)
    if db_class is None:
        new_class = ClassesCreate(class_name=data.class_, key_gbif=data.classKey)
        db_class = await create_class(db, new_class)

    #check if order exists
    db_order = await get_order_by_name(db, data.order)
    if db_order is None:
        new_order = OrdersCreate(order_name=data.order, key_gbif=data.orderKey, class__id=db_class.id)
        db_order = await create_order(db, new_order)

    #check if family exists
    db_family = await get_family_by_name(db, data.family)
    if db_family is None:
        new_family = FamiliesCreate(family_name=data.family, key_gbif=data.familyKey, order_id=db_order.id)
        db_family = await create_family(db, new_family)

    #check if genus exists
    db_genus = await get_genus_by_name(db, data.genus)
    if db_genus is None:
        new_genus = GenusesCreate(genus_name=data.genus, key_gbif=data.genusKey, family_id=db_family.id)
        db_genus = await create_genus(db, new_genus)
        return db_genus

    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Genus already exists")


# create new family  by key of gbif
@router.post(
    path="/api/family_gdif/create",
    tags=["GBIF"],
    response_model= FamiliesResponse,
    status_code=status.HTTP_201_CREATED
    )
async def create_family_by_key(
    key: str,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"])),
)->Family:
    """
    Create a new family by key of gbif
    """
    data  = get_family_details(key)
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Family not found")

    #check if class exists
    db_class = await get_class_by_name(db, data.class_)
    if db_class is None:
        new_class = ClassesCreate(class_name=data.class_, key_gbif=data.classKey)
        db_class = await create_class(db, new_class)

    #check if order exists
    db_order = await get_order_by_name(db, data.order)
    if db_order is None:
        new_order = OrdersCreate(order_name=data.order, key_gbif=data.orderKey, class__id=db_class.id)
        db_order = await create_order(db, new_order)

    #check if family exists
    db_family = await get_family_by_name(db, data.family)
    if db_family is None:
        new_family = FamiliesCreate(family_name=data.family, key_gbif=data.familyKey, order_id=db_order.id)
        db_family = await create_family(db, new_family)
        return db_family

    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Family already exists")

