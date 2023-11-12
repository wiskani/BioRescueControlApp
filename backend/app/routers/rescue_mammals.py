from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Union, Dict

from app.schemas.rescue_mammals import (
    #Habitat
    HabitatBase,
    HabitatCreate,
    HabitatResponse,

    #Rescue Mammals
    RescueMammalsBase,
    RescueMammalsCreate,
    RescueMammalsResponse,

    #Site Release
    SiteReleaseMammalsBase,
    SiteReleaseMammalsCreate,
    SiteReleaseMammalsResponse,

    #Release Mammals
    ReleaseMammalsBase,
    ReleaseMammalsCreate,
    ReleaseMammalsResponse,
)

from  app.models.rescue_mammals import (
    Habitat,
    RescueMammals,
    SiteReleaseMammals,
    ReleaseMammals,
)

from app.crud.rescue_mammals import (
    #Habitat
    get_habitat_name,
    get_habitat_id,
    get_habitats,
    create_habitat,
    update_habitat,
    delete_habitat,

    #Rescue Mammals
    get_rescue_mammal_cod,
    get_rescue_mammal_id,
    get_rescue_mammals,
    create_rescue_mammal,
    update_rescue_mammal,
    delete_rescue_mammal,

    #Site Release
    get_site_release_mammal_name,
    get_site_release_mammal_id,
    get_site_release_mammals,
    create_site_release_mammal,
    update_site_release_mammal,
    delete_site_release_mammal,

    #Release Mammals
    get_release_mammal_cod,
    get_release_mammal_id,
    get_release_mammals,
    create_release_mammal,
    update_release_mammal,
    delete_release_mammal,
)

from app.api.deps import PermissonsChecker, get_db

router: APIRouter = APIRouter()

#Create Habitat 
@router.post(
    path="/api/habitat",
    response_model=HabitatResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Habitat"],
    summary="Create Habitat",
)
async def create_habitat_api(
    new_habitat : HabitatCreate,
    db : AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> Habitat|HTTPException:
    habitat_db = await get_habitat_name(db, new_habitat.name)
    if habitat_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Habitat already exists",
        )
    return await create_habitat(db, new_habitat)

#Get all habitats
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

#Get habitat by id
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
) -> Habitat|HTTPException:
    habitat_db = await get_habitat_id(db, habitat_id)
    if not habitat_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habitat not found",
        )
    return habitat_db

#Update habitat
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
) -> Habitat|HTTPException:
    return await update_habitat(db, habitat_id, habitat_update)

#Delete habitat
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






















