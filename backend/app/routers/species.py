from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Union

from app.schemas.species import(
    Species,
    SpeciesCreate,
    Genuses,
    GenusesCreate,
    Families,
    FamiliesCreate,
    Orders,
    OrdersCreate,
    Classes,
    ClassesCreate,
    SpeciesResponse,
    GenusesResponse,
    FamiliesResponse,
    OrdersResponse,
    ClassesResponse,
    StatusBase,
    StatusResponse,

    #jois
    SpeciesJoin,
)
from app.schemas.rescue_flora import  FloraRescueSpecies
from app.schemas.rescue_mammals import RescueMammalsWithSpecie
from app.schemas.rescue_herpetofauna import TransectHerpetoWithSpecies
from app.models.species import Specie, Genus, Family, Order, Class_, Status
from app.crud.species import (
    # Species
    get_class_id_and_name_by_specie_id,
    get_specie_by_name,
    get_specie_by_name_epithet,
    get_specie_by_id,
    create_specie,
    get_all_species,
    update_specie,
    delete_specie,

    # Genus
    get_genus_by_name,
    get_genus_by_id,
    create_genus,
    get_all_genuses,
    update_genus,
    delete_genus,

    # Family
    get_family_by_name,
    get_family_by_id,
    create_family,
    get_all_families,
    update_family,
    delete_family,

    # Order
    get_order_by_name,
    get_order_by_id,
    create_order,
    get_all_orders,
    update_order,
    delete_order,

    # Class
    get_class_by_name,
    get_class_by_id,
    create_class,
    get_all_classes,
    update_class,
    delete_class,

    # Joins
    get_all_species_join_,

    # Status
    get_status_by_name,
    get_status_by_id,
    create_status,
    get_all_status,
    update_status,
    delete_status,
)
from app.crud.rescue_flora import (
        get_rescue_flora_with_specie_by_specie_id,
        )
from app.crud.rescue_mammals import (
        get_rescue_mammal_list_with_specie_by_specie_id,
        )
from app.crud.rescue_herpetofauna import (
        get_transect_herpetofauna_with_rescues_and_species_by_specie_id,
        )
from app.api.deps import PermissonsChecker, get_db

router: APIRouter = APIRouter()

#Create specie
@router.post(
    path="/api/species",
    response_model=SpeciesResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Species"],
    summary="Create a specie",
)
async def create_a_new_specie(
    new_specie: SpeciesCreate,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> Union[Species, HTTPException]:
    db_specie = await get_specie_by_name(db, new_specie.scientific_name)
    if db_specie:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Specie already exists",
        )
    return await create_specie(db, new_specie)

#Get all species
@router.get(
    path="/api/species",
    response_model=List[SpeciesResponse],
    status_code=status.HTTP_200_OK,
    tags=["Species"],
    summary="Get all species",
)
async def get_all_species_(
    db: AsyncSession  = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin", "read"]))
) -> Union[List[Species], HTTPException]:
    return await get_all_species(db)

#Get specie by id
@router.get(
    path="/api/species/{specie_id}",
    response_model=SpeciesResponse,
    status_code=status.HTTP_200_OK,
    tags=["Species"],
    summary="Get a specie by id",
)
async def get_a_specie_by_id(
    specie_id: int,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> Union[Species, HTTPException]:
    db_specie = await get_specie_by_id(db, specie_id)
    if not db_specie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specie not found",
        )
    return db_specie

#Update specie
@router.put(
    path="/api/species/{specie_id}",
    response_model=SpeciesResponse,
    status_code=status.HTTP_200_OK,
    tags=["Species"],
    summary="Update a specie",
)
async def update_a_specie(
    specie_id: int,
    specie: SpeciesCreate,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> Union[Species, HTTPException]:
    db_specie = await get_specie_by_id(db, specie_id)
    if not db_specie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specie not found",
        )
    return await update_specie(db, specie_id, specie)

#Delete specie
@router.delete(
    path="/api/species/{specie_id}",
    response_model=SpeciesResponse,
    status_code=status.HTTP_200_OK,
    tags=["Species"],
    summary="Delete a specie",
)
async def delete_a_specie(
    specie_id: int,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> Union[Species, HTTPException]:
    db_specie = await get_specie_by_id(db, specie_id)
    if not db_specie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specie not found",
        )
    return await delete_specie(db, specie_id)


#Create genus
@router.post(
    path="/api/genuses",
    response_model=GenusesResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Genuses"],
    summary="Create a genus",
)
async def create_a_new_genus(
    new_genus: GenusesCreate,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> Union[Genuses, HTTPException]:
    db_genus = await get_genus_by_name(db, new_genus.genus_name)
    if db_genus:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Genus already exists",
        )
    return await create_genus(db, new_genus)   

#Get all genuses
@router.get(
    path="/api/genuses",
    response_model=List[GenusesResponse],
    status_code=status.HTTP_200_OK,
    tags=["Genuses"],
    summary="Get all genuses",
)
async def get_all_genuses_(
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> List[Genuses]:
    return await get_all_genuses(db)

#Get genus by id
@router.get(
    path="/api/genuses/{genus_id}",
    response_model=GenusesResponse,
    status_code=status.HTTP_200_OK,
    tags=["Genuses"],
    summary="Get a genus by id",
)
async def get_a_genus_by_id(
    genus_id: int,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> Union[Genuses, HTTPException]:
    db_genus = await get_genus_by_id(db, genus_id)
    if not db_genus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genus not found",
        )
    return db_genus
 
#Update genus
@router.put(
    path="/api/genuses/{genus_id}",
    response_model=GenusesResponse,
    status_code=status.HTTP_200_OK,
    tags=["Genuses"],
    summary="Update a genus",
)
async def update_a_genus(
    genus_id: int,
    genus: GenusesCreate,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> Union[Genuses, HTTPException]:
    db_genus = await get_genus_by_id(db, genus_id)
    if not db_genus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genus not found",
        )
    return await update_genus(db, genus_id, genus)


#Delete genus
@router.delete(
    path="/api/genuses/{genus_id}",
    response_model=GenusesResponse,
    status_code=status.HTTP_200_OK,
    tags=["Genuses"],
    summary="Delete a genus",
)
async def delete_a_genus(
    genus_id: int,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> Union[Genuses, HTTPException]:
    db_genus = await get_genus_by_id(db, genus_id)
    if not db_genus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genus not found",
        )
    return await delete_genus(db, genus_id)

#Create family
@router.post(
    path="/api/families",
    response_model=FamiliesResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Families"],
    summary="Create a family",
)
async def create_a_new_family(
    new_family: FamiliesCreate,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> Union[Families, HTTPException]:
    db_family = await get_family_by_name(db, new_family.family_name)
    if db_family:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Family already exists",
        )
    return await create_family(db, new_family)

#Get all families
@router.get(
    path="/api/families",
    response_model=List[FamiliesResponse],
    status_code=status.HTTP_200_OK,
    tags=["Families"],
    summary="Get all families",
)
async def get_all_families_(
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> List[Family]:
    return await get_all_families(db)

#Get family by id
@router.get(
    path="/api/families/{family_id}",
    response_model=Families,
    status_code=status.HTTP_200_OK,
    tags=["Families"],
    summary="Get a family by id",
)
async def get_a_family_by_id(
    family_id: int,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> Union[Families, HTTPException]:
    db_family = await get_family_by_id(db, family_id)
    if not db_family:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Family not found",
        )
    return db_family

#Update family
@router.put(
    path="/api/families/{family_id}",
    response_model=FamiliesResponse,
    status_code=status.HTTP_200_OK,
    tags=["Families"],
    summary="Update a family",
)
async def update_a_family(
    family_id: int,
    family: FamiliesCreate,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> Union[Families, HTTPException]:
    db_family = await get_family_by_id(db, family_id)
    if not db_family:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Family not found",
        )
    return await update_family(db, family_id, family)

#Delete family
@router.delete(
    path="/api/families/{family_id}",
    response_model=FamiliesResponse,
    status_code=status.HTTP_200_OK,
    tags=["Families"],
    summary="Delete a family",
)
async def delete_a_family(
    family_id: int,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> Union[Families, HTTPException]:
    db_family = await get_family_by_id(db, family_id)
    if not db_family:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Family not found",
        )
    return await delete_family(db, family_id)

#Create order
@router.post(
    path="/api/orders",
    response_model=OrdersResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Orders"],
    summary="Create a order",
)
async def create_a_new_order(
    new_order: OrdersCreate,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> Union[Orders, HTTPException]:
    db_order = await get_order_by_name(db, new_order.order_name)
    if db_order:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Order already exists",
        )
    return await create_order(db, new_order)

#Get all orders
@router.get(
    path="/api/orders",
    response_model=List[OrdersResponse],
    status_code=status.HTTP_200_OK,
    tags=["Orders"],
    summary="Get all orders",
)
async def get_all_orders_(
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> List[Order]:
    return await get_all_orders(db)

#Get order by id
@router.get(
    path="/api/orders/{order_id}",
    response_model=OrdersResponse,
    status_code=status.HTTP_200_OK,
    tags=["Orders"],
    summary="Get a order by id",
)
async def get_a_order_by_id(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> Union[Orders, HTTPException]:
    db_order = await get_order_by_id(db, order_id)
    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    return db_order

#Update order
@router.put(
    path="/api/orders/{order_id}",
    response_model=OrdersResponse,
    status_code=status.HTTP_200_OK,
    tags=["Orders"],
    summary="Update a order",
)
async def update_a_order(
    order_id: int,
    order: OrdersCreate,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> Union[Orders, HTTPException]:
    db_order = await get_order_by_id(db, order_id)
    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    return await update_order(db, order_id, order)

#Delete order
@router.delete(
    path="/api/orders/{order_id}",
    response_model=OrdersResponse,
    status_code=status.HTTP_200_OK,
    tags=["Orders"],
    summary="Delete a order",
)
async def delete_a_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> Union[Orders, HTTPException]:
    db_order = await get_order_by_id(db, order_id)
    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    return await delete_order(db, order_id)

#Create Class
@router.post(
    path="/api/classes",
    response_model=ClassesResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Classes"],
    summary="Create a class",
)
async def create_a_new_class(
    new_class: ClassesCreate,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> Union[Classes, HTTPException]:
    db_class = await get_class_by_name(db, new_class.class_name)
    if db_class:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Class already exists",
        )
    return await create_class(db, new_class)

#Get all classes
@router.get(
    path="/api/classes",
    response_model=List[ClassesResponse],
    status_code=status.HTTP_200_OK,
    tags=["Classes"],
    summary="Get all classes",
)
async def get_all_classes_(
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> List[Class_]:
    classes = await get_all_classes(db)
    return classes

#Get class by id
@router.get(
    path="/api/classes/{class_id}",
    response_model=ClassesResponse,
    status_code=status.HTTP_200_OK,
    tags=["Classes"],
    summary="Get a class by id",
)
async def get_a_class_by_id(
    class_id: int,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> Union[Classes, HTTPException]:
    db_class = await get_class_by_id(db, class_id)
    if not db_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found",
        )
    return db_class

#Update class
@router.put(
    path="/api/classes/{class_id}",
    response_model=ClassesResponse,
    status_code=status.HTTP_200_OK,
    tags=["Classes"],
    summary="Update a class",
)
async def update_a_class(
    class_id: int,
    class_: ClassesCreate,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> Union[Classes, HTTPException]:
    db_class = await get_class_by_id(db, class_id)
    if not db_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found",
        )
    return await update_class(db, class_id, class_)

#Delete class
@router.delete(
    path="/api/classes/{class_id}",
    response_model=ClassesResponse,
    status_code=status.HTTP_200_OK,
    tags=["Classes"],
    summary="Delete a class",
)
async def delete_a_class(
    class_id: int,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> Union[Classes, HTTPException]:
    db_class = await get_class_by_id(db, class_id)
    if not db_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found",
        )
    return await delete_class(db, class_id)

# Endpoint for species join endpoint
@router.get(
    path="/api/join/species",
    response_model=List[SpeciesJoin],
    status_code=status.HTTP_200_OK,
    tags=["Species"],
    summary="Get all species with all their information",
)
async def get_all_species_join(
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> List[SpeciesJoin]:
    return await get_all_species_join_(db)

#Create Status
@router.post(
    path="/api/specie/status",
    response_model=StatusResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Status"],
    summary="Create a status",
)
async def create_a_new_status(
    new_status: StatusBase,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> Union[Status, HTTPException]:
    db_status = await get_status_by_name(db, new_status.status_name)
    if db_status:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Status already exists",
        )
    return await create_status(db, new_status)

#Get all status
@router.get(
    path="/api/specie/status",
    response_model=List[StatusResponse],
    status_code=status.HTTP_200_OK,
    tags=["Status"],
    summary="Get all status",
)
async def get_all_status_(
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> List[Status]:
    return await get_all_status(db)

#Get status by id
@router.get(
    path="/api/specie/status/{status_id}",
    response_model=StatusResponse,
    status_code=status.HTTP_200_OK,
    tags=["Status"],
    summary="Get a status by id",
)
async def get_a_status_by_id(
    status_id: int,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> Union[Status, HTTPException]:
    db_status = await get_status_by_id(db, status_id)
    if not db_status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Status not found",
        )
    return db_status

#Update status
@router.put(
    path="/api/specie/status/{status_id}",
    response_model=StatusResponse,
    status_code=status.HTTP_200_OK,
    tags=["Status"],
    summary="Update a status",
)
async def update_a_status(
    status_id: int,
    status_: StatusBase,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> Union[Status, HTTPException]:
    db_status = await get_status_by_id(db, status_id)
    if not db_status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Status not found",
        )
    return await update_status(db, status_id, status_)

#Delete status
@router.delete(
    path="/api/specie/status/{status_id}",
    response_model=StatusResponse,
    status_code=status.HTTP_200_OK,
    tags=["Status"],
    summary="Delete a status",
)
async def delete_a_status(
    status_id: int,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> Union[Status, HTTPException]:
    db_status = await get_status_by_id(db, status_id)
    if not db_status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Status not found",
        )
    return await delete_status(db, status_id)


#Get rescues by specie name
@router.get(
    path="/api/specie/rescues/{specie_id}",
    response_model=List[FloraRescueSpecies]| List[RescueMammalsWithSpecie]| List[TransectHerpetoWithSpecies],
    status_code=status.HTTP_200_OK,
    tags=["Species"],
    summary="Get all rescues by specie name",
)
async def get_all_rescues_by_specie_name(
    specie_id: int,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> List[FloraRescueSpecies] | List[RescueMammalsWithSpecie] | List[TransectHerpetoWithSpecies] | HTTPException:
    #Check if specie exists
    db_specie = await get_specie_by_id(db, specie_id)
    if not db_specie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specie not found",
        )

    #get class_ by specie id 
    db_class = await get_class_id_and_name_by_specie_id(db, specie_id)

    if not db_class:
        return db_class

    if db_class.class_name == "Mammalia":
        return await get_rescue_mammal_list_with_specie_by_specie_id(db, specie_id)

    if db_class.class_name == "Liliopsida" or db_class.class_name == "Polypodiopsida ":
        return await get_rescue_flora_with_specie_by_specie_id(db, specie_id)

    if db_class.class_name == "Amphibia" or db_class.class_name == "Reptilia":
        return await get_transect_herpetofauna_with_rescues_and_species_by_specie_id(db, specie_id)
    










