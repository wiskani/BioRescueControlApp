from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import func, select, delete
from typing import List, Union, Optional
from fastapi import HTTPException

from app.schemas.species import (
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
    SpeciesJoin,
    StatusBase,
    StatusResponse,
)
from app.models.species import Specie, Genus, Family, Order, Class_, Status
from app.models.rescue_flora import FloraRescue
from app.models.images import Image

#Purpose: CRUD operations for Species

#Get if specie exists
async def get_specie_by_name(db: AsyncSession, scientific_name: str) -> Specie | None:
    specie_db= await db.execute(select(Specie).where(Specie.scientific_name == scientific_name))
    return specie_db.scalars().first()

#Create a specie
async def create_specie(db: AsyncSession, specie: SpeciesCreate) -> Specie:
    db_specie = Specie(
        scientific_name = specie.scientific_name,
        specific_epithet = specie.specific_epithet,
        key_gbif = specie.key_gbif,
        status_id = specie.status_id,
        genus_id = specie.genus_id

    )
    db.add(db_specie)
    await db.commit()
    await db.refresh(db_specie)
    return db_specie

#Get all species
async def get_all_species(db: AsyncSession) -> List[Specie]:
    species_db = await db.execute(select(Specie))
    return list(species_db.scalars().all())

#Get specie by id
async def get_specie_by_id(db: AsyncSession, specie_id: int) -> Union[Specie, None]:
    specie_db = await db.execute(select(Specie).filter(Specie.id == specie_id))
    return specie_db.scalars().first()

#Update specie
async def update_specie(db: AsyncSession, specie_id: int, specie: SpeciesCreate) -> Specie:
    db_specie = await get_specie_by_id(db, specie_id)
    if not db_specie:
        raise HTTPException(status_code=404, detail="Specie not found")
    db_specie.scientific_name = specie.scientific_name
    db_specie.specific_epithet = specie.specific_epithet
    db_specie.key_gbif = specie.key_gbif
    db_specie.status_id = specie.status_id
    db_specie.genus_id = specie.genus_id
    await db.commit()
    await db.refresh(db_specie)
    return db_specie

#Delete specie
async def delete_specie(db: AsyncSession, specie_id: int) -> Specie:
    db_specie = await get_specie_by_id(db, specie_id)
    if not db_specie:
        raise HTTPException(status_code=404, detail="Specie not found")
    await db.execute(delete(Specie).where(Specie.id == specie_id))
    await db.commit()
    return db_specie

#Create a genus
async def create_genus(db: AsyncSession, genus: GenusesCreate) -> Genus:
    db_genus = Genus(
        genus_name = genus.genus_name,
        key_gbif = genus.key_gbif,
        family_id = genus.family_id
    )
    db.add(db_genus)
    await db.commit()
    await db.refresh(db_genus)
    return db_genus

#Get all genuses
async def get_all_genuses(db: AsyncSession) -> List[Genus]:
    genuses_db = await db.execute(select(Genus))
    return list(genuses_db.scalars().all())

#Get genus by id
async def get_genus_by_id(db: AsyncSession, genus_id: int) -> Genus | None:
    genus_db = await db.execute(select(Genus).filter(Genus.id == genus_id))
    return genus_db.scalars().first()

#Get genus by name
async def get_genus_by_name(db: AsyncSession, genus_name: str) -> Genus | None:
    genus_db = await db.execute(select(Genus).filter(Genus.genus_name == genus_name))
    return genus_db.scalars().first()

#Update genus
async def update_genus(db: AsyncSession, genus_id: int, genus: GenusesCreate) -> Genus:
    db_genus = await get_genus_by_id(db, genus_id)
    if not db_genus:
        raise HTTPException(status_code=404, detail="Genus not found")
    db_genus.genus_name = genus.genus_name
    db_genus.key_gbif = genus.key_gbif
    db_genus.family_id = genus.family_id
    await db.commit()
    await db.refresh(db_genus)
    return db_genus

#Delete genus
async def delete_genus(db: AsyncSession, genus_id: int) -> Genus:
    db_genus = await get_genus_by_id(db, genus_id)
    if not db_genus:
        raise HTTPException(status_code=404, detail="Genus not found")
    await db.execute(delete(Genus).where(Genus.id == genus_id))
    await db.commit()
    return db_genus

#Create a family
async def create_family(db: AsyncSession, family: FamiliesCreate) -> Family:
    db_family = Family(
        family_name = family.family_name,
        key_gbif = family.key_gbif,
        order_id = family.order_id
    )
    db.add(db_family)
    await db.commit()
    await db.refresh(db_family)
    return db_family

#Get all families
async def get_all_families(db: AsyncSession) -> List[Family]:
    families_db = await db.execute(select(Family))
    return list(families_db.scalars().all())

#Get family by id
async def get_family_by_id(db: AsyncSession, family_id: int) -> Family | None:
    family_db = await db.execute(select(Family).filter(Family.id == family_id))
    return family_db.scalars().first()

#Get family by name
async def get_family_by_name(db: AsyncSession, family_name: str) -> Union[Family, None]:
    family_db = await db.execute(select(Family).filter(Family.family_name == family_name))
    return family_db.scalars().first()

#Update family
async def update_family(db: AsyncSession, family_id: int, family: FamiliesCreate) -> Family:
    db_family = await get_family_by_id(db, family_id)
    if not db_family:
        raise HTTPException(status_code=404, detail="Family not found")
    db_family.family_name = family.family_name
    db_family.key_gbif = family.key_gbif
    db_family.order_id = family.order_id
    await db.commit()
    await db.refresh(db_family)
    return db_family

#Delete family
async def delete_family(db: AsyncSession, family_id: int) -> Family:
    db_family = await get_family_by_id(db, family_id)
    if not db_family:
        raise HTTPException(status_code=404, detail="Family not found")
    await db.execute(delete(Family).where(Family.id == family_id))
    await db.commit()
    return db_family

#Create an order
async def create_order(db: AsyncSession, order: OrdersCreate) -> Order:
    db_order = Order(
        order_name = order.order_name,
        key_gbif = order.key_gbif,
        class__id = order.class__id
    )
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order

#Get all orders
async def get_all_orders(db: AsyncSession) -> List[Order]:
    orders_db = await db.execute(select(Order))
    return list(orders_db.scalars().all())

#Get order by id
async def get_order_by_id(db: AsyncSession, order_id: int) -> Union[Order, None]:
    order_db = await db.execute(select(Order).filter(Order.id == order_id))
    return order_db.scalars().first()

#Get order by name
async def get_order_by_name(db: AsyncSession, order_name: str) -> Union[Order, None]:
    order_db = await db.execute(select(Order).filter(Order.order_name == order_name))
    return order_db.scalars().first()

#Update order
async def update_order(db: AsyncSession, order_id: int, order: OrdersCreate) -> Order:
    db_order = await get_order_by_id(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db_order.order_name = order.order_name
    db_order.key_gbif = order.key_gbif
    db_order.class__id = order.class__id
    await db.commit()
    await db.refresh(db_order)
    return db_order

#Delete order
async def delete_order(db: AsyncSession, order_id: int) -> Order:
    db_order = await get_order_by_id(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    await db.execute(delete(Order).where(Order.id == order_id))
    await db.commit()
    return db_order

#Create a class
async def create_class(db: AsyncSession, class_: ClassesCreate) -> Class_:
    db_class = Class_(
        class_name = class_.class_name,
        key_gbif = class_.key_gbif,
    )
    db.add(db_class)
    await db.commit()
    await db.refresh(db_class)
    return db_class

#Get all classes    
async def get_all_classes(db: AsyncSession) -> List[Class_]:
    classes_db = await db.execute(select(Class_))
    return list(classes_db.scalars().all())

#Get class by id
async def get_class_by_id(db: AsyncSession, class_id: int) -> Class_ | None:
    class_db = await db.execute(select(Class_).filter(Class_.id == class_id))
    return class_db.scalars().first()

#Get class by name
async def get_class_by_name(db: AsyncSession, class_name: str) -> Union[Class_, None]:
    class_db = await db.execute(select(Class_).filter(Class_.class_name == class_name))
    return class_db.scalars().first()

#Update class
async def update_class(db: AsyncSession, class_id: int, class_: ClassesCreate) -> Class_:
    db_class = await get_class_by_id(db, class_id)
    if not db_class:
        raise HTTPException(status_code=404, detail="Class not found")
    db_class.class_name = class_.class_name
    db_class.key_gbif = class_.key_gbif
    await db.commit()
    await db.refresh(db_class)
    return db_class

#Delete class
async def delete_class(db: AsyncSession, class_id: int) -> Class_:
    db_class = await get_class_by_id(db, class_id)
    if not db_class:
        raise HTTPException(status_code=404, detail="Class not found")
    await db.execute(delete(Class_).where(Class_.id == class_id))
    await db.commit()
    return db_class

#Get if status exists
async def get_status_by_name(db: AsyncSession, status_name: str) -> Union[Status, None]:
    status_db = await db.execute(select(Status).filter(Status.status_name == status_name))
    return status_db.scalars().first()

#Create a status
async def create_status(db: AsyncSession, status: StatusBase) -> Status:
    db_status = Status(
        status_name = status.status_name,
    )
    db.add(db_status)
    await db.commit()
    await db.refresh(db_status)
    return db_status

#Get all status
async def get_all_status(db: AsyncSession) -> List[Status]:
    status_db = await db.execute(select(Status))
    return list(status_db.scalars().all())

#Get status by id
async def get_status_by_id(db: AsyncSession, status_id: int) -> Union[Status, None]:
    status_db = await db.execute(select(Status).filter(Status.id == status_id))
    return status_db.scalars().first()

#Update status
async def update_status(db: AsyncSession, status_id: int, status: StatusBase) -> Status:
    db_status = await get_status_by_id(db, status_id)
    if not db_status:
        raise HTTPException(status_code=404, detail="Status not found")
    db_status.status_name = status.status_name
    await db.commit()
    await db.refresh(db_status)
    return db_status

#Delete status
async def delete_status(db: AsyncSession, status_id: int) -> Status:
    db_status = await get_status_by_id(db, status_id)
    if not db_status:
        raise HTTPException(status_code=404, detail="Status not found")
    await db.execute(delete(Status).where(Status.id == status_id))
    await db.commit()
    return db_status


#Make a join species and all other tables
async def get_all_species_join_(db: AsyncSession) -> List[SpeciesJoin]:
    species_result = await db.execute(select(Specie))
    species = species_result.scalars().all()

    result = []
    for specie in species:
        # Cargar las relaciones de forma individual
        genus = await db.get(Genus, specie.genus_id)
        family = await db.get(Family, genus.family_id) if genus else None
        order = await db.get(Order, family.order_id) if family else None
        class_ = await db.get(Class_, order.class__id) if order else None

        # Cargar imágenes de manera individual
        images_result = await db.execute(select(Image).where(Image.species_id == specie.id))
        images_data = images_result.scalars().all()

        total_rescues = await count_flora_rescue_by_specie(db, specie.id)
        images_data = [
            {
                "attribute": image.atribute,
                "url": image.url,
                "species_id": specie.id
            }
            for image in images_data
        ]
        result.append({
            "scientific_name": specie.scientific_name,
            "specie_name": specie.specific_epithet,
            "genus_full_name": genus.genus_name if genus else None,
            "family_name": family.family_name if family else None,
            "order_name": order.order_name if order else None,
            "class_name": class_.class_name if class_ else None,
            "images": images_data,
            "total_rescues": total_rescues
        })
    return result

#Count flora_rescue by specie
async def count_flora_rescue_by_specie(db: AsyncSession, specie_id:int) -> int :
    if not specie_id:
        return 0
    stmt = select(func.count(FloraRescue.id)).where(FloraRescue.specie_epiphyte_id == specie_id)

    result = await db.execute(stmt)

    total= result.scalar()

    if total is None:
        return 0

    return total






