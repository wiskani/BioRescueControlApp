from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Union, Dict

from app.schemas.rescue_flora import (
        FloraRescueZoneBase,
        FloraRescueZoneResponse,

        FloraRelocationZoneBase,
        FloraRelocationZoneResponse,

        FloraRescueBase,
        FloraRescueResponse,

        PlantNurseryBase,
        PlantNurseryResponse,

        FloraRelocationBase,
        FloraRelocationResponse,

        FloraRescueSpecies,
        FloraRelocationWithSpecie
        )
from app.models.rescue_flora import (
    PlantNursery,
)

from app.crud.rescue_flora import (
        # Rescue Zone
        get_flora_rescue_zone,
        get_flora_rescue_zone_by_id,
        get_all_flora_rescue_zones,
        create_flora_rescue_zone,
        update_flora_rescue_zone,
        delete_flora_rescue_zone,

        # Relocation Zone
        get_flora_relocation_zone,
        get_flora_relocation_zone_by_id,
        get_all_flora_relocation_zones,
        create_flora_relocation_zone,
        update_flora_relocation_zone,
        delete_flora_relocation_zone,

        # Rescue
        get_flora_rescue,
        get_flora_rescue_by_id,
        get_all_flora_rescues,
        create_flora_rescue,
        update_flora_rescue,
        delete_flora_rescue,

        # Plant Nursery
        get_plant_nursery,
        get_plant_nursery_by_id,
        get_all_plant_nurseries,
        create_plant_nursery,
        update_plant_nursery,
        delete_plant_nursery,

        # Relocation
        get_flora_relocation,
        get_flora_relocation_by_id,
        get_all_flora_relocations,
        create_flora_relocation,
        update_flora_relocation,
        delete_flora_relocation,

        # Rescue with species
        get_rescue_flora_with_specie,
        get_rescue_flora_with_specie_by_epiphyte_number,

        # Relocation with species
        get_all_translocation_with_specie,
        get_translocation_with_specie_by_epiphyte_number
)

from app.api.deps import PermissonsChecker, get_db

router: APIRouter = APIRouter()

"""
ENDPOINTS FOR RESCUE ZONE
"""


# Create a rescue zone endpoint
@router.post(
        path="/api/rescue_flora/rescue_zone",
        response_model=FloraRescueZoneResponse,
        status_code=status.HTTP_201_CREATED,
        tags=["Rescue Zone"],
        summary="Create a rescue zone",
)
async def create_a_new_rescue_zone(
        rescue_zone: FloraRescueZoneBase,
        db: AsyncSession = Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        ) -> Union[FloraRescueZoneResponse, HTTPException]:

    db_rescue_zone = await get_flora_rescue_zone(db, rescue_zone.name)
    if db_rescue_zone:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rescue zone already exists",
                )
    rescue_zona_new = await create_flora_rescue_zone(db, rescue_zone)

    rescue_zone_new_db = FloraRescueZoneResponse(
            id=rescue_zona_new.id,
            name=rescue_zona_new.name,
            description=rescue_zona_new.description,
            )

    return rescue_zone_new_db


# Get all rescue zones endpoint
@router.get(
        path="/api/rescue_flora/rescue_zone",
        response_model=List[FloraRescueZoneResponse],
        status_code=status.HTTP_200_OK,
        tags=["Rescue Zone"],
        summary="Get all rescue zones",
)
async def get_all_rescue_zones_(
        db: AsyncSession = Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        ) -> Union[List[FloraRescueZoneResponse], HTTPException]:
    return await get_all_flora_rescue_zones(db)


# Get a rescue zone by id endpoint
@router.get(
        path="/api/rescue_flora/rescue_zone/{rescue_zone_id}",
        response_model=FloraRescueZoneResponse,
        status_code=status.HTTP_200_OK,
        tags=["Rescue Zone"],
        summary="Get a rescue zone by id",
)
async def get_a_rescue_zone_by_id(
        rescue_zone_id: int,
        db: AsyncSession = Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        ) -> Union[FloraRescueZoneResponse, HTTPException]:
    db_rescue_zone = await get_flora_rescue_zone_by_id(db, rescue_zone_id)
    if not db_rescue_zone:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rescue zone not found",
                )
    db_rescue_zone = FloraRescueZoneResponse(
            id=db_rescue_zone.id,
            name=db_rescue_zone.name,
            description=db_rescue_zone.description,
            )
    return db_rescue_zone


# Update a rescue zone endpoint
@router.put(
        path="/api/rescue_flora/rescue_zone/{rescue_zone_id}",
        response_model=FloraRescueZoneResponse,
        status_code=status.HTTP_200_OK,
        tags=["Rescue Zone"],
        summary="Update a rescue zone",
)
async def update_a_rescue_zone(
        rescue_zone_id: int,
        rescue_zone: FloraRescueZoneBase,
        db: AsyncSession = Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        ) -> Union[FloraRescueZoneResponse, HTTPException]:
    db_rescue_zone = await get_flora_rescue_zone_by_id(db, rescue_zone_id)
    if not db_rescue_zone:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rescue zone not found",
                )
    return await update_flora_rescue_zone(db, rescue_zone_id, rescue_zone)


# Delete a rescue zone endpoint
@router.delete(
        path="/api/rescue_flora/rescue_zone/{rescue_zone_id}",
        status_code=status.HTTP_200_OK,
        tags=["Rescue Zone"],
        summary="Delete a rescue zone",
)
async def delete_a_rescue_zone(
        rescue_zone_id: int,
        db: AsyncSession = Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        ) -> Dict:
    db_rescue_zone = await get_flora_rescue_zone_by_id(db, rescue_zone_id)
    if not db_rescue_zone:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rescue zone not found",
                )
    await delete_flora_rescue_zone(db, rescue_zone_id)
    return {"detail": "Rescue zone deleted"}

"""
ENDPOINTS FOR RELOCATION ZONE
"""


# Create a relocation zone endpoint
@router.post(
        path="/api/rescue_flora/relocation_zone",
        response_model=FloraRelocationZoneResponse,
        status_code=status.HTTP_201_CREATED,
        tags=["Relocation Zone"],
        summary="Create a relocation zone",
)
async def create_a_new_relocation_zone(
        relocation_zone: FloraRelocationZoneBase,
        db: AsyncSession = Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        ) -> Union[FloraRelocationZoneResponse, HTTPException]:

    db_relocation_zone = await get_flora_relocation_zone(db, relocation_zone.name)
    if db_relocation_zone:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Relocation zone already exists",
                )
    return await create_flora_relocation_zone(db, relocation_zone)


# Get all relocation zones endpoint
@router.get(
        path="/api/rescue_flora/relocation_zone",
        response_model=List[FloraRelocationZoneResponse],
        status_code=status.HTTP_200_OK,
        tags=["Relocation Zone"],
        summary="Get all relocation zones",
)
async def get_all_relocation_zones_(
        db:AsyncSession=Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        )->Union[List[FloraRelocationZoneResponse], HTTPException]:
    return await get_all_flora_relocation_zones(db)

#Get a relocation zone by id endpoint
@router.get(
        path="/api/rescue_flora/relocation_zone/{relocation_zone_id}",
        response_model=FloraRelocationZoneResponse,
        status_code=status.HTTP_200_OK,
        tags=["Relocation Zone"],
        summary="Get a relocation zone by id",
)
async def get_a_relocation_zone_by_id(
        relocation_zone_id:int,
        db:AsyncSession=Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        )->Union[FloraRelocationZoneResponse, HTTPException]:
    db_relocation_zone = await get_flora_relocation_zone_by_id(db, relocation_zone_id)
    if not db_relocation_zone:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Relocation zone not found",
                )
    return db_relocation_zone

#Update a relocation zone endpoint
@router.put(
        path="/api/rescue_flora/relocation_zone/{relocation_zone_id}",
        response_model=FloraRelocationZoneResponse,
        status_code=status.HTTP_200_OK,
        tags=["Relocation Zone"],
        summary="Update a relocation zone",
)
async def update_a_relocation_zone(
        relocation_zone_id:int,
        relocation_zone:FloraRelocationZoneBase,
        db:AsyncSession=Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        )->Union[FloraRelocationZoneResponse, HTTPException]:
    db_relocation_zone = await get_flora_relocation_zone_by_id(db, relocation_zone_id)
    if not db_relocation_zone:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Relocation zone not found",
                )
    return await update_flora_relocation_zone(db, relocation_zone_id, relocation_zone)

#Delete a relocation zone endpoint
@router.delete(
        path="/api/rescue_flora/relocation_zone/{relocation_zone_id}",
        status_code=status.HTTP_200_OK,
        tags=["Relocation Zone"],
        summary="Delete a relocation zone",
)
async def delete_a_relocation_zone(
        relocation_zone_id:int,
        db:AsyncSession=Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        )->Dict:
    db_relocation_zone = await get_flora_relocation_zone_by_id(db, relocation_zone_id)
    if not db_relocation_zone:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Relocation zone not found",
                )
    await delete_flora_relocation_zone(db, relocation_zone_id)
    return {"detail":"Relocation zone deleted"}


"""
ENDPOINTS FOR FLORA RESCUE
"""

#Create a flora rescue endpoint
@router.post(
        path="/api/rescue_flora",
        response_model=FloraRescueResponse,
        status_code=status.HTTP_201_CREATED,
        tags=["Flora Rescue"],
        summary="Create a flora rescue",
)
async def create_a_new_flora_rescue(
        flora_rescue:FloraRescueBase,
        db:AsyncSession=Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        )->Union[FloraRescueResponse, HTTPException]:

    db_flora_rescue = await get_flora_rescue(db, flora_rescue.epiphyte_number)
    if db_flora_rescue:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Flora rescue already exists",
                )
    return await create_flora_rescue(db, flora_rescue)

#Get all flora rescues endpoint
@router.get(
        path="/api/rescue_flora",
        response_model=List[FloraRescueResponse],
        status_code=status.HTTP_200_OK,
        tags=["Flora Rescue"],
        summary="Get all flora rescues",
)
async def get_all_flora_rescues_(
        db:AsyncSession=Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        )->Union[List[FloraRescueResponse], HTTPException]:
    return await get_all_flora_rescues(db)

#Get a flora rescue by id endpoint
@router.get(
        path="/api/rescue_flora/{flora_rescue_id}",
        response_model=FloraRescueResponse,
        status_code=status.HTTP_200_OK,
        tags=["Flora Rescue"],
        summary="Get a flora rescue by id",
)
async def get_a_flora_rescue_by_id(
        flora_rescue_id:int,
        db:AsyncSession=Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        )->Union[FloraRescueResponse, HTTPException]:
    db_flora_rescue = await get_flora_rescue_by_id(db, flora_rescue_id)
    if not db_flora_rescue:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Flora rescue not found",
                )
    return db_flora_rescue

#Update a flora rescue endpoint
@router.put(
        path="/api/rescue_flora/{flora_rescue_id}",
        response_model=FloraRescueResponse,
        status_code=status.HTTP_200_OK,
        tags=["Flora Rescue"],
        summary="Update a flora rescue",
)
async def update_a_flora_rescue(
        flora_rescue_id:int,
        flora_rescue:FloraRescueBase,
        db:AsyncSession=Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        )->Union[FloraRescueResponse, HTTPException]:
    db_flora_rescue = await get_flora_rescue_by_id(db, flora_rescue_id)
    if not db_flora_rescue:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Flora rescue not found",
                )
    return await update_flora_rescue(db, flora_rescue_id, flora_rescue)

#Delete a flora rescue endpoint
@router.delete(
        path="/api/rescue_flora/{flora_rescue_id}",
        status_code=status.HTTP_200_OK,
        tags=["Flora Rescue"],
        summary="Delete a flora rescue",
)
async def delete_a_flora_rescue(
        flora_rescue_id:int,
        db:AsyncSession=Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        )->Dict:
    db_flora_rescue = await get_flora_rescue_by_id(db, flora_rescue_id)
    if not db_flora_rescue:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Flora rescue not found",
                )
    await delete_flora_rescue(db, flora_rescue_id)
    return {"detail":"Flora rescue deleted"}

"""
ENDPOINTS FOR PLANT NURSERY
"""

#Create a plant nursery endpoint
@router.post(
        path="/api/rescue_flora/plant_nursery",
        response_model=PlantNurseryResponse,
        status_code=status.HTTP_201_CREATED,
        tags=["Plant Nursery"],
        summary="Create a plant nursery",
)
async def create_a_new_plant_nursery(
        plant_nursery:PlantNurseryBase,
        db:AsyncSession=Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        )->Union[PlantNurseryResponse, HTTPException]:

    db_plant_nursery = await get_plant_nursery(db, plant_nursery.cod_reg)
    if db_plant_nursery:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Plant nursery already exists",
                )
    return await create_plant_nursery(db, plant_nursery)

#Get all plant nurseries endpoint
@router.get(
        path="/api/plant_nurseries",
        response_model=List[PlantNurseryResponse],
        status_code=status.HTTP_200_OK,
        tags=["Plant Nursery"],
        summary="Get all plant nurseries",
)
async def get_all_plant_nurseries_(
        db:AsyncSession=Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        )->List[PlantNursery]:
    return await get_all_plant_nurseries(db)

#Get a plant nursery by id endpoint
@router.get(
        path="/api/rescue_flora/plant_nursery/{plant_nursery_id}",
        response_model=PlantNurseryResponse,
        status_code=status.HTTP_200_OK,
        tags=["Plant Nursery"],
        summary="Get a plant nursery by id",
)
async def get_a_plant_nursery_by_id(
        plant_nursery_id:int,
        db:AsyncSession=Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        )->Union[PlantNurseryResponse, HTTPException]:
    db_plant_nursery = await get_plant_nursery_by_id(db, plant_nursery_id)
    if not db_plant_nursery:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plant nursery not found",
                )
    return db_plant_nursery

#Update a plant nursery endpoint
@router.put(
        path="/api/rescue_flora/plant_nursery/{plant_nursery_id}",
        response_model=PlantNurseryResponse,
        status_code=status.HTTP_200_OK,
        tags=["Plant Nursery"],
        summary="Update a plant nursery",
)
async def update_a_plant_nursery(
        plant_nursery_id:int,
        plant_nursery:PlantNurseryBase,
        db:AsyncSession=Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        )->Union[PlantNurseryResponse, HTTPException]:
    db_plant_nursery = await get_plant_nursery_by_id(db, plant_nursery_id)
    if not db_plant_nursery:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plant nursery not found",
                )
    return await update_plant_nursery(db, plant_nursery_id, plant_nursery)


# Delete a plant nursery endpoint
@router.delete(
        path="/api/rescue_flora/plant_nursery/{plant_nursery_id}",
        status_code=status.HTTP_200_OK,
        tags=["Plant Nursery"],
        summary="Delete a plant nursery",
)
async def delete_a_plant_nursery(
        plant_nursery_id: int,
        db: AsyncSession = Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        ) -> Dict:
    db_plant_nursery = await get_plant_nursery_by_id(db, plant_nursery_id)
    if not db_plant_nursery:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plant nursery not found",
                )
    await delete_plant_nursery(db, plant_nursery_id)
    return {"detail": "Plant nursery deleted"}

"""
ENDPOINTS FOR FLORA RELOCATION
"""


# Create a new flora relocation endpoint
@router.post(
        path="/api/flora_relocation",
        response_model=FloraRelocationResponse,
        status_code=status.HTTP_201_CREATED,
        tags=["Flora Relocation"],
        summary="Create a new flora relocation",
)
async def create_a_new_flora_relocation(
        flora_relocation: FloraRelocationBase,
        db: AsyncSession = Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        ) -> Union[FloraRelocationResponse, HTTPException]:

    db_flora_relocation = await get_flora_relocation(
            db,
            flora_relocation.relocation_number
            )
    if db_flora_relocation:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Flora relocation already exists",
                )
    return await create_flora_relocation(db, flora_relocation)


# Get all flora relocations endpoint
@router.get(
        path="/api/flora_relocations",
        response_model=List[FloraRelocationResponse],
        status_code=status.HTTP_200_OK,
        tags=["Flora Relocation"],
        summary="Get all flora relocations",
)
async def get_all_flora_relocations_(
        db: AsyncSession = Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        ) -> Union[List[FloraRelocationResponse], HTTPException]:
    return await get_all_flora_relocations(db)


# Get a flora relocation by id endpoint
@router.get(
        path="/api/flora_relocation/{flora_relocation_id}",
        response_model=FloraRelocationResponse,
        status_code=status.HTTP_200_OK,
        tags=["Flora Relocation"],
        summary="Get a flora relocation by id",
)
async def get_a_flora_relocation_by_id(
        flora_relocation_id: int,
        db: AsyncSession = Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        ) -> FloraRelocationResponse | HTTPException:
    db_flora_relocation = await get_flora_relocation_by_id(
            db,
            flora_relocation_id
            )
    if not db_flora_relocation:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Flora relocation not found",
                )
    return db_flora_relocation


# Update a flora relocation endpoint
@router.put(
        path="/api/flora_relocation/{flora_relocation_id}",
        response_model=FloraRelocationResponse,
        status_code=status.HTTP_200_OK,
        tags=["Flora Relocation"],
        summary="Update a flora relocation",
)
async def update_a_flora_relocation(
        flora_relocation_id: int,
        flora_relocation: FloraRelocationBase,
        db: AsyncSession = Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        ) -> Union[FloraRelocationResponse, HTTPException]:
    db_flora_relocation = await get_flora_relocation_by_id(
            db,
            flora_relocation_id
            )
    if not db_flora_relocation:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Flora relocation not found",
                )
    return await update_flora_relocation(
            db,
            flora_relocation_id,
            flora_relocation
            )


# Delete a flora relocation endpoint
@router.delete(
        path="/api/flora_relocation/{flora_relocation_id}",
        status_code=status.HTTP_200_OK,
        tags=["Flora Relocation"],
        summary="Delete a flora relocation",
)
async def delete_a_flora_relocation(
        flora_relocation_id: int,
        db: AsyncSession = Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        ) -> Dict:
    db_flora_relocation = await get_flora_relocation_by_id(
            db,
            flora_relocation_id
            )
    if not db_flora_relocation:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Flora relocation not found",
                )
    await delete_flora_relocation(db, flora_relocation_id)
    return {"detail": "Flora relocation deleted"}


# Get all flora rescues with species, genus and family endpoint
@router.get(
        path="/api/flora_rescue_species",
        response_model=List[FloraRescueSpecies],
        status_code=status.HTTP_200_OK,
        tags=["Flora Rescue"],
        summary="Get all flora rescues with species, genus and family",
)
async def get_all_flora_rescue_species(
        db: AsyncSession = Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        ) -> List[FloraRescueSpecies]:
    return await get_rescue_flora_with_specie(db)


# Get all translocation with species and extra data
@router.get(
        path="/api/flora_relocation_with_specie",
        response_model=List[FloraRelocationWithSpecie],
        status_code=status.HTTP_200_OK,
        tags=["Flora Relocation"],
        summary="Get all flora relocations with species and extra data",
)
async def get_all_flora_relocation_with_specie(
        db: AsyncSession = Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        ) -> List[FloraRelocationWithSpecie] | HTTPException:
    return await get_all_translocation_with_specie(db)


# Get flora rescues with species, genus and family endpoint by epiphyte number
@router.get(
        path="/api/flora_rescue_species/{epiphyte_number}",
        response_model=FloraRescueSpecies,
        status_code=status.HTTP_200_OK,
        tags=["Flora Rescue"],
        summary="Get flora rescues with species, genus and family by epiphyte number",
)
async def get_flora_rescue_species_by_epiphyte_number_api(
        epiphyte_number: str,
        db: AsyncSession = Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        ) -> FloraRescueSpecies | HTTPException:
    return await get_rescue_flora_with_specie_by_epiphyte_number(
            db,
            epiphyte_number
            )


# Get translocation with species and extra data by epiphyte number
@router.get(
        path="/api/flora_relocation_with_specie/{epiphyte_number}",
        response_model=FloraRelocationWithSpecie | dict,
        status_code=status.HTTP_200_OK,
        tags=["Flora Relocation"],
        summary="Get translocation with species and extra data by epiphyte number",
)
async def get_flora_relocation_with_specie_by_epiphyte_number_api(
        epiphyte_number: str,
        db: AsyncSession = Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        ) -> FloraRelocationWithSpecie | HTTPException | dict:
    return await get_translocation_with_specie_by_epiphyte_number(
            db,
            epiphyte_number
            )
