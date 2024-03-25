from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Union, Dict

from app.schemas.rescue_mammals import (
    # Habitat
    HabitatCreate,
    HabitatResponse,

    # Rescue Mammals
    RescueMammalsCreate,
    RescueMammalsResponse,

    # Site Release
    SiteReleaseMammalsCreate,
    SiteReleaseMammalsResponse,

    # Release Mammals
    ReleaseMammalsCreate,
    ReleaseMammalsResponse,

    # Rescue Mammals with species
    RescueMammalsWithSpecie
)

from app.models.rescue_mammals import (
    Habitat,
    RescueMammals,
    SiteReleaseMammals,
    ReleaseMammals,
)

from app.crud.rescue_mammals import (
    # Habitat
    get_habitat_name,
    get_habitat_id,
    get_habitats,
    create_habitat,
    update_habitat,
    delete_habitat,

    # Rescue Mammals
    get_rescue_mammal_cod,
    get_rescue_mammal_id,
    get_rescue_mammals,
    create_rescue_mammal,
    update_rescue_mammal,
    delete_rescue_mammal,

    # Site Release
    get_site_release_mammal_name,
    get_site_release_mammal_id,
    get_site_release_mammals,
    create_site_release_mammal,
    update_site_release_mammal,
    delete_site_release_mammal,

    # Release Mammals
    get_release_mammal_cod,
    get_release_mammal_id,
    get_release_mammals,
    create_release_mammal,
    update_release_mammal,
    delete_release_mammal,

    # Rescue Mammals with species
    get_rescue_mammals_with_specie
)

from app.api.deps import PermissonsChecker, get_db

router: APIRouter = APIRouter()


# Create Habitat
@router.post(
    path="/api/habitat",
    response_model=HabitatResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Habitat"],
    summary="Create Habitat",
)
async def create_habitat_api(
    new_habitat: HabitatCreate,
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> Habitat | HTTPException:
    habitat_db = await get_habitat_name(db, new_habitat.name)
    if habitat_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Habitat already exists",
        )
    return await create_habitat(db, new_habitat)


# Get all habitats
@router.get(
    path="/api/habitat",
    response_model=List[HabitatResponse],
    status_code=status.HTTP_200_OK,
    tags=["Habitat"],
    summary="Get all habitats",
    )
async def get_habitats_api(
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin", "user"])),
) -> List[Habitat]:
    return await get_habitats(db)


# Get habitat by id
@router.get(
    path="/api/habitat/{habitat_id}",
    response_model=HabitatResponse,
    status_code=status.HTTP_200_OK,
    tags=["Habitat"],
    summary="Get habitat by id",
)
async def get_habitat_by_id_api(
    habitat_id: int,
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin", "user"])),
) -> Habitat | HTTPException:
    habitat_db = await get_habitat_id(db, habitat_id)
    if not habitat_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habitat not found",
        )
    return habitat_db


# Update habitat
@router.put(
    path="/api/habitat/{habitat_id}",
    response_model=HabitatResponse,
    status_code=status.HTTP_200_OK,
    tags=["Habitat"],
    summary="Update habitat",
)
async def update_habitat_api(
    habitat_id: int,
    habitat_update: HabitatCreate,
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> Habitat | HTTPException:
    return await update_habitat(db, habitat_id, habitat_update)


# Delete habitat
@router.delete(
    path="/api/habitat/{habitat_id}",
    response_model= None,
    status_code=status.HTTP_200_OK,
    tags=["Habitat"],
    summary="Delete habitat",
)
async def delete_habitat_api(
    habitat_id: int,
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> Habitat|HTTPException:
    habitat_db = await get_habitat_id(db, habitat_id)
    if not habitat_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habitat not found",
        )
    await delete_habitat(db, habitat_id)
    return {"detail": "Habitat deleted successfully"}

#Create Rescue Mammals
@router.post(
    path="/api/rescue_mammals",
    response_model=RescueMammalsResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Rescue Mammals"],
    summary="Create Rescue Mammals",
)
async def create_rescue_mammals_api(
    new_rescue_mammals : RescueMammalsCreate,
    db : AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> RescueMammals|HTTPException:
    rescue_mammals_db = await get_rescue_mammal_cod(db, new_rescue_mammals.cod)
    if rescue_mammals_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Rescue mammal already exists",
        )
    return await create_rescue_mammal(db, new_rescue_mammals)

#Get all Rescue Mammals
@router.get(
    path="/api/rescue_mammals",
    response_model=List[RescueMammalsResponse],
    status_code=status.HTTP_200_OK,
    tags=["Rescue Mammals"],
    summary="Get all Rescue Mammals",
    )
async def get_rescue_mammals_api(
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin", "user"])),
) -> List[RescueMammals]:
    return await get_rescue_mammals(db)

#Get Rescue Mammals by id
@router.get(
    path="/api/rescue_mammals/{rescue_mammals_id}",
    response_model=RescueMammalsResponse,
    status_code=status.HTTP_200_OK,
    tags=["Rescue Mammals"],
    summary="Get Rescue Mammals by id",
)
async def get_rescue_mammals_by_id_api(
    rescue_mammals_id: int,
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin", "user"])),
) -> RescueMammals|HTTPException:
    rescue_mammals_db = await get_rescue_mammal_id(db, rescue_mammals_id)
    if not rescue_mammals_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rescue Mammals not found",
        )
    return rescue_mammals_db

#Update Rescue Mammals
@router.put(
    path="/api/rescue_mammals/{rescue_mammals_id}",
    response_model=RescueMammalsResponse,
    status_code=status.HTTP_200_OK,
    tags=["Rescue Mammals"],
    summary="Update Rescue Mammals",
)
async def update_rescue_mammals_api(
    rescue_mammals_id: int,
    rescue_mammals_update: RescueMammalsCreate,
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> RescueMammals|HTTPException:
    return await update_rescue_mammal(db, rescue_mammals_id, rescue_mammals_update)

#Delete Rescue Mammals
@router.delete(
    path="/api/rescue_mammals/{rescue_mammals_id}",
    response_model= None,
    status_code=status.HTTP_200_OK,
    tags=["Rescue Mammals"],
    summary="Delete Rescue Mammals",
)
async def delete_rescue_mammals_api(
    rescue_mammals_id: int,
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> RescueMammals|HTTPException:
    rescue_mammals_db = await get_rescue_mammal_id(db, rescue_mammals_id)
    if not rescue_mammals_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rescue Mammals not found",
        )
    await delete_rescue_mammal(db, rescue_mammals_id)
    return {"detail": "Rescue Mammals deleted successfully"}

#Create site release mammals
@router.post(
    path="/api/site_release_mammals",
    response_model=SiteReleaseMammalsResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Site Release Mammals"],
    summary="Create Site Release Mammals",
)
async def create_site_release_mammals_api(
    new_site_release_mammals : SiteReleaseMammalsCreate,
    db : AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> SiteReleaseMammals|HTTPException:
    site_release_mammals_db = await get_site_release_mammal_name(db, new_site_release_mammals.name)
    if site_release_mammals_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Site release mammal already exists",
        )
    return await create_site_release_mammal(db, new_site_release_mammals)

#Get all Site Release Mammals
@router.get(
    path="/api/site_release_mammals",
    response_model=List[SiteReleaseMammalsResponse],
    status_code=status.HTTP_200_OK,
    tags=["Site Release Mammals"],
    summary="Get all Site Release Mammals",
    )
async def get_site_release_mammals_api(
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin", "user"])),
) -> List[SiteReleaseMammals]:
    return await get_site_release_mammals(db)

#Get Site Release Mammals by id
@router.get(
    path="/api/site_release_mammals/{site_release_mammals_id}",
    response_model=SiteReleaseMammalsResponse,
    status_code=status.HTTP_200_OK,
    tags=["Site Release Mammals"],
    summary="Get Site Release Mammals by id",
)
async def get_site_release_mammals_by_id_api(
    site_release_mammals_id: int,
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin", "user"])),
) -> SiteReleaseMammals|HTTPException:
    site_release_mammals_db = await get_site_release_mammal_id(db, site_release_mammals_id)
    if not site_release_mammals_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site Release Mammals not found",
        )
    return site_release_mammals_db

#Update Site Release Mammals
@router.put(
    path="/api/site_release_mammals/{site_release_mammals_id}",
    response_model=SiteReleaseMammalsResponse,
    status_code=status.HTTP_200_OK,
    tags=["Site Release Mammals"],
    summary="Update Site Release Mammals",
)
async def update_site_release_mammals_api(
    site_release_mammals_id: int,
    site_release_mammals_update: SiteReleaseMammalsCreate,
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> SiteReleaseMammals|HTTPException:
    return await update_site_release_mammal(db, site_release_mammals_id, site_release_mammals_update)

#Delete Site Release Mammals
@router.delete(
    path="/api/site_release_mammals/{site_release_mammals_id}",
    response_model= None,
    status_code=status.HTTP_200_OK,
    tags=["Site Release Mammals"],
    summary="Delete Site Release Mammals",
)
async def delete_site_release_mammals_api(
    site_release_mammals_id: int,
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> SiteReleaseMammals|HTTPException:
    site_release_mammals_db = await get_site_release_mammal_id(db, site_release_mammals_id)
    if not site_release_mammals_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site Release Mammals not found",
        )
    await delete_site_release_mammal(db, site_release_mammals_id)
    return {"detail": "Site Release Mammals deleted successfully"}

#Create site mammals
@router.post(
    path="/api/release_mammals",
    response_model=ReleaseMammalsResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Release Mammals"],
    summary="Create Release Mammals",
)
async def create_release_mammals_api(
    new_release_mammals : ReleaseMammalsCreate,
    db : AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> ReleaseMammals|HTTPException:
    release_mammals_db = await get_release_mammal_cod(db, new_release_mammals.cod)
    if release_mammals_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Release mammal already exists",
        )
    return await create_release_mammal(db, new_release_mammals)

#Get all Release Mammals
@router.get(
    path="/api/release_mammals",
    response_model=List[ReleaseMammalsResponse],
    status_code=status.HTTP_200_OK,
    tags=["Release Mammals"],
    summary="Get all Release Mammals",
    )
async def get_release_mammals_api(
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin", "user"])),
) -> List[ReleaseMammals]:
    return await get_release_mammals(db)

#Get Release Mammals by id
@router.get(
    path="/api/release_mammals/{release_mammals_id}",
    response_model=ReleaseMammalsResponse,
    status_code=status.HTTP_200_OK,
    tags=["Release Mammals"],
    summary="Get Release Mammals by id",
)
async def get_release_mammals_by_id_api(
    release_mammals_id: int,
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin", "user"])),
) -> ReleaseMammals|HTTPException:
    release_mammals_db = await get_release_mammal_id(db, release_mammals_id)
    if not release_mammals_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Release Mammals not found",
        )
    return release_mammals_db

#Update Release Mammals
@router.put(
    path="/api/release_mammals/{release_mammals_id}",
    response_model=ReleaseMammalsResponse,
    status_code=status.HTTP_200_OK,
    tags=["Release Mammals"],
    summary="Update Release Mammals",
)
async def update_release_mammals_api(
    release_mammals_id: int,
    release_mammals_update: ReleaseMammalsCreate,
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> ReleaseMammals|HTTPException:
    return await update_release_mammal(db, release_mammals_id, release_mammals_update)

#Delete Release Mammals
@router.delete(
    path="/api/release_mammals/{release_mammals_id}",
    response_model= None,
    status_code=status.HTTP_200_OK,
    tags=["Release Mammals"],
    summary="Delete Release Mammals",
)
async def delete_release_mammals_api(
    release_mammals_id: int,
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> ReleaseMammals|HTTPException:
    release_mammals_db = await get_release_mammal_id(db, release_mammals_id)
    if not release_mammals_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Release Mammals not found",
        )
    await delete_release_mammal(db, release_mammals_id)
    return {"detail": "Release Mammals deleted successfully"}

#Get all rescue mammals with species
@router.get(
    path="/api/rescue_mammals_species",
    response_model=List[RescueMammalsWithSpecie],
    status_code=status.HTTP_200_OK,
    tags=["Rescue Mammals"],
    summary="Get all rescue mammals with species",
    )
async def get_rescue_mammals_with_species_api(
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> List[RescueMammalsWithSpecie]:
    return await get_rescue_mammals_with_specie(db)


























