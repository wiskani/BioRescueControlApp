from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
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
        ) 
from app.models.rescue_flora import FloraRescueZone, FloraRelocationZone, FloraRescue, PlantNursery, FloraRelocation

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
)

from app.api.deps import PermissonsChecker, get_db

router:APIRouter = APIRouter()

"""
ENDPOINTS FOR RESCUE ZONE
"""

#Create a rescue zone endpoint
@router.post(
        path="/api/rescue_flora/rescue_zone",
        response_model=FloraRescueZoneResponse,
        status_code=status.HTTP_201_CREATED,
        tags=["Rescue Zone"],
        summary="Create a rescue zone",
)
async def create_a_new_rescue_zone(
        rescue_zone:FloraRescueZoneBase,
        db:Session=Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        )->Union[FloraRescueZoneResponse, HTTPException]:

    db_rescue_zone = await get_flora_rescue_zone(db, rescue_zone.name)
    if db_rescue_zone:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rescue zone already exists",
                )
    return await create_flora_rescue_zone(db, rescue_zone)

#Get all rescue zones endpoint
@router.get(
        path="/api/rescue_flora/rescue_zone",
        response_model=List[FloraRescueZoneResponse],
        status_code=status.HTTP_200_OK,
        tags=["Rescue Zone"],
        summary="Get all rescue zones",
)
async def get_all_rescue_zones_(
        db:Session=Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        )->Union[List[FloraRescueZoneResponse], HTTPException]:
    return await get_all_flora_rescue_zones(db)

#Get a rescue zone by id endpoint
@router.get(
        path="/api/rescue_flora/rescue_zone/{rescue_zone_id}",
        response_model=FloraRescueZoneResponse,
        status_code=status.HTTP_200_OK,
        tags=["Rescue Zone"],
        summary="Get a rescue zone by id",
)
async def get_a_rescue_zone_by_id(
        rescue_zone_id:int,
        db:Session=Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        )->Union[FloraRescueZoneResponse, HTTPException]:
    db_rescue_zone = await get_flora_rescue_zone_by_id(db, rescue_zone_id)
    if not db_rescue_zone:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rescue zone not found",
                )
    return db_rescue_zone

#Update a rescue zone endpoint
@router.put(
        path="/api/rescue_flora/rescue_zone/{rescue_zone_id}",
        response_model=FloraRescueZoneResponse,
        status_code=status.HTTP_200_OK,
        tags=["Rescue Zone"],
        summary="Update a rescue zone",
)
async def update_a_rescue_zone(
        rescue_zone_id:int,
        rescue_zone:FloraRescueZoneBase,
        db:Session=Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        )->Union[FloraRescueZoneResponse, HTTPException]:
    db_rescue_zone = await get_flora_rescue_zone_by_id(db, rescue_zone_id)
    if not db_rescue_zone:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rescue zone not found",
                )
    return await update_flora_rescue_zone(db, rescue_zone_id, rescue_zone)

#Delete a rescue zone endpoint
@router.delete(
        path="/api/rescue_flora/rescue_zone/{rescue_zone_id}",
        status_code=status.HTTP_200_OK,
        tags=["Rescue Zone"],
        summary="Delete a rescue zone",
)
async def delete_a_rescue_zone(
        rescue_zone_id:int,
        db:Session=Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        )->Dict:
    db_rescue_zone = await get_flora_rescue_zone_by_id(db, rescue_zone_id)
    if not db_rescue_zone:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rescue zone not found",
                )
    await delete_flora_rescue_zone(db, rescue_zone_id)
    return {"detail":"Rescue zone deleted"}

"""
ENDPOINTS FOR RELOCATION ZONE
"""

#Create a relocation zone endpoint
@router.post(
        path="/api/rescue_flora/relocation_zone",
        response_model=FloraRelocationZoneResponse,
        status_code=status.HTTP_201_CREATED,
        tags=["Relocation Zone"],
        summary="Create a relocation zone",
)
async def create_a_new_relocation_zone(
        relocation_zone:FloraRelocationZoneBase,
        db:Session=Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        )->Union[FloraRelocationZoneResponse, HTTPException]:

    db_relocation_zone = await get_flora_relocation_zone(db, relocation_zone.name)
    if db_relocation_zone:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Relocation zone already exists",
                )
    return await create_flora_relocation_zone(db, relocation_zone)

#Get all relocation zones endpoint
@router.get(
        path="/api/rescue_flora/relocation_zone",
        response_model=List[FloraRelocationZoneResponse],
        status_code=status.HTTP_200_OK,
        tags=["Relocation Zone"],
        summary="Get all relocation zones",
)
async def get_all_relocation_zones_(
        db:Session=Depends(get_db),
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
        db:Session=Depends(get_db),
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
        db:Session=Depends(get_db),
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
        db:Session=Depends(get_db),
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
        db:Session=Depends(get_db),
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
        db:Session=Depends(get_db),
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
        db:Session=Depends(get_db),
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
        db:Session=Depends(get_db),
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
        db:Session=Depends(get_db),
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
        db:Session=Depends(get_db),
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
        path="/api/rescue_flora/plant_nursery",
        response_model=List[PlantNurseryResponse],
        status_code=status.HTTP_200_OK,
        tags=["Plant Nursery"],
        summary="Get all plant nurseries",
)
async def get_all_plant_nurseries_(
        db:Session=Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        )->Union[List[PlantNurseryResponse], HTTPException]:
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
        db:Session=Depends(get_db),
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
        db:Session=Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        )->Union[PlantNurseryResponse, HTTPException]:
    db_plant_nursery = await get_plant_nursery_by_id(db, plant_nursery_id)
    if not db_plant_nursery:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plant nursery not found",
                )
    return await update_plant_nursery(db, plant_nursery_id, plant_nursery)

#Delete a plant nursery endpoint
@router.delete(
        path="/api/rescue_flora/plant_nursery/{plant_nursery_id}",
        status_code=status.HTTP_200_OK,
        tags=["Plant Nursery"],
        summary="Delete a plant nursery",
)
async def delete_a_plant_nursery(
        plant_nursery_id:int,
        db:Session=Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        )->Dict:
    db_plant_nursery = await get_plant_nursery_by_id(db, plant_nursery_id)
    if not db_plant_nursery:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plant nursery not found",
                )
    await delete_plant_nursery(db, plant_nursery_id)
    return {"detail":"Plant nursery deleted"}

#Create a new flora relocation endpoint
@router.post(
        path="/api/rescue_flora/flora_relocation",
        response_model=FloraRelocationResponse,
        status_code=status.HTTP_201_CREATED,
        tags=["Flora Relocation"],
        summary="Create a new flora relocation",
)
async def create_a_new_flora_relocation(
        flora_relocation:FloraRelocationBase,
        db:Session=Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        )->Union[FloraRelocationResponse, HTTPException]:

    db_flora_relocation = await get_flora_relocation(db, flora_relocation.relocation_number)
    if db_flora_relocation:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Flora relocation already exists",
                )
    return await create_flora_relocation(db, flora_relocation)

#Get all flora relocations endpoint
@router.get(
        path="/api/rescue_flora/flora_relocation",
        response_model=List[FloraRelocationResponse],
        status_code=status.HTTP_200_OK,
        tags=["Flora Relocation"],
        summary="Get all flora relocations",
)
async def get_all_flora_relocations_(
        db:Session=Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        )->Union[List[FloraRelocationResponse], HTTPException]:
    return await get_all_flora_relocations(db)

#Get a flora relocation by id endpoint
@router.get(
        path="/api/rescue_flora/flora_relocation/{flora_relocation_id}",
        response_model=FloraRelocationResponse,
        status_code=status.HTTP_200_OK,
        tags=["Flora Relocation"],
        summary="Get a flora relocation by id",
)
async def get_a_flora_relocation_by_id(
        flora_relocation_id:int,
        db:Session=Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        )->Union[FloraRelocationResponse, HTTPException]:
    db_flora_relocation = await get_flora_relocation_by_id(db, flora_relocation_id)
    if not db_flora_relocation:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Flora relocation not found",
                )
    return db_flora_relocation

#Update a flora relocation endpoint
@router.put(
        path="/api/rescue_flora/flora_relocation/{flora_relocation_id}",
        response_model=FloraRelocationResponse,
        status_code=status.HTTP_200_OK,
        tags=["Flora Relocation"],
        summary="Update a flora relocation",
)
async def update_a_flora_relocation(
        flora_relocation_id:int,
        flora_relocation:FloraRelocationBase,
        db:Session=Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        )->Union[FloraRelocationResponse, HTTPException]:
    db_flora_relocation = await get_flora_relocation_by_id(db, flora_relocation_id)
    if not db_flora_relocation:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Flora relocation not found",
                )
    return await update_flora_relocation(db, flora_relocation_id, flora_relocation)

#Delete a flora relocation endpoint
@router.delete(
        path="/api/rescue_flora/flora_relocation/{flora_relocation_id}",
        status_code=status.HTTP_200_OK,
        tags=["Flora Relocation"],
        summary="Delete a flora relocation",
)
async def delete_a_flora_relocation(
        flora_relocation_id:int,
        db:Session=Depends(get_db),
        autorized: bool = Depends(PermissonsChecker(["admin"])),
        )->Dict:
    db_flora_relocation = await get_flora_relocation_by_id(db, flora_relocation_id)
    if not db_flora_relocation:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Flora relocation not found",
                )
    await delete_flora_relocation(db, flora_relocation_id)
    return {"detail":"Flora relocation deleted"}





















