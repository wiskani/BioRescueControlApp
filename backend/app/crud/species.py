from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, delete
from typing import List, Union
from fastapi import HTTPException

from app.schemas.species import (
    SpeciesCreate,
    GenusesCreate,
    FamiliesCreate,
    OrdersCreate,
    ClassesCreate,
    SpeciesJoin,
    StatusBase,
)
from app.schemas.images import ImageBase
from app.models.species import Specie, Genus, Family, Order, Class_, Status
from app.models.rescue_flora import FloraRescue
from app.models.rescue_herpetofauna import RescueHerpetofauna
from app.models.rescue_mammals import RescueMammals
from app.models.images import Image

# Purpose: CRUD operations for Species


async def get_specie_by_name(
        db: AsyncSession,
        scientific_name: str
        ) -> Specie | None:
    """Get a specie by its scientific name"""
    specie_db = await db.execute(
            select(Specie)
            .where(Specie.scientific_name == scientific_name)
            )
    return specie_db.scalars().first()


async def get_specie_by_name_epithet(
        db: AsyncSession,
        name: str
        ) -> Specie | None:
    """Get a specie by its specific epithet"""
    specie_db = await db.execute(
            select(Specie)
            .where(Specie.specific_epithet == name)
            )
    return specie_db.scalars().first()


async def create_specie(db: AsyncSession, specie: SpeciesCreate) -> Specie:
    """Create a new specie"""
    db_specie = Specie(
        scientific_name=specie.scientific_name,
        specific_epithet=specie.specific_epithet,
        key_gbif=specie.key_gbif,
        status_id=specie.status_id,
        genus_id=specie.genus_id
    )
    db.add(db_specie)
    await db.commit()
    await db.refresh(db_specie)
    return db_specie


async def get_all_species(db: AsyncSession) -> List[Specie]:
    """Get all species"""
    species_db = await db.execute(select(Specie))
    return list(species_db.scalars().all())


async def get_specie_by_id(
        db: AsyncSession, specie_id: int) -> Union[Specie, None]:
    """Get a specie by its id"""
    specie_db = await db.execute(select(Specie).filter(Specie.id == specie_id))
    return specie_db.scalars().first()


async def update_specie(
        db: AsyncSession,
        specie_id: int,
        specie: SpeciesCreate
        ) -> Specie:
    """Update a specie"""
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


async def delete_specie(db: AsyncSession, specie_id: int) -> Specie:
    """Delete a specie"""
    db_specie = await get_specie_by_id(db, specie_id)
    if not db_specie:
        raise HTTPException(status_code=404, detail="Specie not found")
    await db.execute(delete(Specie).where(Specie.id == specie_id))
    await db.commit()
    return db_specie


async def create_genus(db: AsyncSession, genus: GenusesCreate) -> Genus:
    """Create a new genus"""
    db_genus = Genus(
        genus_name=genus.genus_name,
        key_gbif=genus.key_gbif,
        family_id=genus.family_id
    )
    db.add(db_genus)
    await db.commit()
    await db.refresh(db_genus)
    return db_genus


async def get_all_genuses(db: AsyncSession) -> List[Genus]:
    """Get all genuses"""
    genuses_db = await db.execute(select(Genus))
    return list(genuses_db.scalars().all())


async def get_genus_by_id(db: AsyncSession, genus_id: int) -> Genus | None:
    """Get a genus by its id"""
    genus_db = await db.execute(select(Genus).filter(Genus.id == genus_id))
    return genus_db.scalars().first()


async def get_genus_by_name(db: AsyncSession, genus_name: str) -> Genus | None:
    """Get a genus by its name"""
    genus_db = await db.execute(
            select(Genus)
            .filter(Genus.genus_name == genus_name)
            )
    return genus_db.scalars().first()


async def update_genus(
        db: AsyncSession,
        genus_id: int,
        genus: GenusesCreate
        ) -> Genus:
    """Update a genus"""
    db_genus = await get_genus_by_id(db, genus_id)
    if not db_genus:
        raise HTTPException(status_code=404, detail="Genus not found")
    db_genus.genus_name = genus.genus_name
    db_genus.key_gbif = genus.key_gbif
    db_genus.family_id = genus.family_id
    await db.commit()
    await db.refresh(db_genus)
    return db_genus


async def delete_genus(db: AsyncSession, genus_id: int) -> Genus:
    """Delete a genus"""
    db_genus = await get_genus_by_id(db, genus_id)
    if not db_genus:
        raise HTTPException(status_code=404, detail="Genus not found")
    await db.execute(delete(Genus).where(Genus.id == genus_id))
    await db.commit()
    return db_genus


async def create_family(db: AsyncSession, family: FamiliesCreate) -> Family:
    """Create a new family"""
    db_family = Family(
        family_name=family.family_name,
        key_gbif=family.key_gbif,
        order_id=family.order_id
    )
    db.add(db_family)
    await db.commit()
    await db.refresh(db_family)
    return db_family


async def get_all_families(db: AsyncSession) -> List[Family]:
    """Get all families"""
    families_db = await db.execute(select(Family))
    return list(families_db.scalars().all())


async def get_family_by_id(db: AsyncSession, family_id: int) -> Family | None:
    """Get a family by its id"""
    family_db = await db.execute(select(Family).filter(Family.id == family_id))
    return family_db.scalars().first()


async def get_family_by_name(
        db: AsyncSession,
        family_name: str
        ) -> Family | None:
    """Get a family by its name"""
    family_db = await db.execute(
            select(Family).filter(Family.family_name == family_name)
            )
    return family_db.scalars().first()


async def update_family(
        db: AsyncSession,
        family_id: int,
        family: FamiliesCreate
        ) -> Family:
    """Update a family"""
    db_family = await get_family_by_id(db, family_id)
    if not db_family:
        raise HTTPException(status_code=404, detail="Family not found")
    db_family.family_name = family.family_name
    db_family.key_gbif = family.key_gbif
    db_family.order_id = family.order_id
    await db.commit()
    await db.refresh(db_family)
    return db_family


async def delete_family(db: AsyncSession, family_id: int) -> Family:
    """Delete a family"""
    db_family = await get_family_by_id(db, family_id)
    if not db_family:
        raise HTTPException(status_code=404, detail="Family not found")
    await db.execute(delete(Family).where(Family.id == family_id))
    await db.commit()
    return db_family


async def create_order(db: AsyncSession, order: OrdersCreate) -> Order:
    """Create a new order"""
    db_order = Order(
        order_name=order.order_name,
        key_gbif=order.key_gbif,
        class__id=order.class__id
    )
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order


async def get_all_orders(db: AsyncSession) -> List[Order]:
    """Get all orders"""
    orders_db = await db.execute(select(Order))
    return list(orders_db.scalars().all())


async def get_order_by_id(db: AsyncSession, order_id: int) -> Order | None:
    """Get a order by its id"""
    order_db = await db.execute(select(Order).filter(Order.id == order_id))
    return order_db.scalars().first()


async def get_order_by_name(db: AsyncSession, order_name: str) -> Order | None:
    """Get a order by its name"""
    order_db = await db.execute(
            select(Order).filter(Order.order_name == order_name)
            )
    return order_db.scalars().first()


async def update_order(
        db: AsyncSession,
        order_id: int,
        order: OrdersCreate
        ) -> Order:
    """Update a order"""
    db_order = await get_order_by_id(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db_order.order_name = order.order_name
    db_order.key_gbif = order.key_gbif
    db_order.class__id = order.class__id
    await db.commit()
    await db.refresh(db_order)
    return db_order


async def delete_order(db: AsyncSession, order_id: int) -> Order:
    """Delete a order"""
    db_order = await get_order_by_id(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    await db.execute(delete(Order).where(Order.id == order_id))
    await db.commit()
    return db_order


async def create_class(db: AsyncSession, class_: ClassesCreate) -> Class_:
    """Create a new class"""
    db_class = Class_(
        class_name=class_.class_name,
        key_gbif=class_.key_gbif,
    )
    db.add(db_class)
    await db.commit()
    await db.refresh(db_class)
    return db_class


async def get_all_classes(db: AsyncSession) -> List[Class_]:
    """Get all classes"""
    classes_db = await db.execute(select(Class_))
    return list(classes_db.scalars().all())


async def get_class_by_id(db: AsyncSession, class_id: int) -> Class_ | None:
    """Get a class by its id"""
    class_db = await db.execute(select(Class_).filter(Class_.id == class_id))
    return class_db.scalars().first()


async def get_class_by_name(
        db: AsyncSession,
        class_name: str
        ) -> Class_ | None:
    """Get a class by its name"""
    class_db = await db.execute(
            select(Class_).filter(Class_.class_name == class_name)
            )
    return class_db.scalars().first()


async def update_class(
        db: AsyncSession,
        class_id: int,
        class_: ClassesCreate
        ) -> Class_:
    """Update a class"""
    db_class = await get_class_by_id(db, class_id)
    if not db_class:
        raise HTTPException(status_code=404, detail="Class not found")
    db_class.class_name = class_.class_name
    db_class.key_gbif = class_.key_gbif
    await db.commit()
    await db.refresh(db_class)
    return db_class


async def delete_class(db: AsyncSession, class_id: int) -> Class_:
    """Delete a class"""
    db_class = await get_class_by_id(db, class_id)
    if not db_class:
        raise HTTPException(status_code=404, detail="Class not found")
    await db.execute(delete(Class_).where(Class_.id == class_id))
    await db.commit()
    return db_class


async def get_status_by_name(
        db: AsyncSession,
        status_name: str
        ) -> Status | None:
    """Get a status by its name"""
    status_db = await db.execute(
            select(Status).filter(Status.status_name == status_name)
            )
    return status_db.scalars().first()


async def create_status(
        db: AsyncSession,
        status: StatusBase
        ) -> Status:
    """Create a new status"""
    db_status = Status(
        status_name=status.status_name,
    )
    db.add(db_status)
    await db.commit()
    await db.refresh(db_status)
    return db_status


async def get_all_status(db: AsyncSession) -> List[Status]:
    """Get all status"""
    status_db = await db.execute(select(Status))
    return list(status_db.scalars().all())


async def get_status_by_id(db: AsyncSession, status_id: int) -> Status | None:
    """Get a status by its id"""
    status_db = await db.execute(select(Status).filter(Status.id == status_id))
    return status_db.scalars().first()


async def update_status(
        db: AsyncSession,
        status_id: int,
        status: StatusBase
        ) -> Status:
    """Update a status"""
    db_status = await get_status_by_id(db, status_id)
    if not db_status:
        raise HTTPException(status_code=404, detail="Status not found")
    db_status.status_name = status.status_name
    await db.commit()
    await db.refresh(db_status)
    return db_status


async def delete_status(db: AsyncSession, status_id: int) -> Status:
    """Delete a status"""
    db_status = await get_status_by_id(db, status_id)
    if not db_status:
        raise HTTPException(status_code=404, detail="Status not found")
    await db.execute(delete(Status).where(Status.id == status_id))
    await db.commit()
    return db_status


async def get_all_species_join_(db: AsyncSession) -> List[SpeciesJoin]:
    """Get all species join with all other tables"""
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
        images_result = await db.execute(
                select(Image).where(Image.species_id == specie.id)
                )
        images_data = list(images_result.scalars().all())

        total_rescues = await count_flora_rescue_by_specie(db, specie.id)
        if total_rescues == 0:
            total_rescues = await count_herpetofauna_rescue_by_specie(
                    db,
                    specie.id
                    )
            if total_rescues == 0:
                total_rescues = await count_mammal_rescue_by_specie(
                        db,
                        specie.id
                        )
        image_list = []
        for image in images_data:
            db_image = ImageBase(
                atribute=image.atribute,
                url=image.url,
                species_id=specie.id
            )
            image_list.append(db_image)

        if not class_:
            raise HTTPException(status_code=404, detail="Class not found")
        if class_.class_name in ("Magnoliopsida", "Pinopsida"):
            pass
        elif total_rescues > 0:
            db_specie = SpeciesJoin(
                id=specie.id,
                scientific_name=specie.scientific_name,
                specie_name=specie.specific_epithet,
                genus_full_name=genus.genus_name if genus else None,
                family_name=family.family_name if family else None,
                order_name=order.order_name if order else None,
                class_name=class_.class_name if class_ else None,
                images=image_list,
                total_rescues=total_rescues
            )
            result.append(db_specie)
    return result

# Count flora_rescue by specie


async def count_flora_rescue_by_specie(
        db: AsyncSession,
        specie_id: int
        ) -> int:
    if not specie_id:
        return 0
    stmt = select(
            func.count(FloraRescue.id)
            ).where(
                    FloraRescue.specie_epiphyte_id == specie_id
                    )

    result = await db.execute(stmt)

    total = result.scalar()

    if total is None:
        return 0

    return total

# Count herpetofauna rescue by specie


async def count_herpetofauna_rescue_by_specie(
        db: AsyncSession,
        specie_id: int
        ) -> int:
    if not specie_id:
        return 0
    stmt = select(
            func.count(RescueHerpetofauna.id)
            ).where(
                    RescueHerpetofauna.specie_id == specie_id
                    )

    result = await db.execute(stmt)

    total = result.scalar()

    if total is None:
        return 0

    return total

# Count mammal rescue by specie


async def count_mammal_rescue_by_specie(
        db: AsyncSession,
        specie_id: int
        ) -> int:
    if not specie_id:
        return 0
    stmt = select(
            func.count(RescueMammals.id)
            ).where(
                    RescueMammals.specie_id == specie_id
                    )

    result = await db.execute(stmt)

    total = result.scalar()

    if total is None:
        return 0

    return total

# List of species by family


async def get_species_by_family(db: AsyncSession, family_id: int) -> List[int]:
    genus_result = await db.execute(
            select(Genus).where(Genus.family_id == family_id)
            )
    genus = genus_result.scalars().all()
    result = []
    for gen in genus:
        species_result = await db.execute(
                select(Specie).where(Specie.genus_id == gen.id)
                )
        species = species_result.scalars().all()
        for specie in species:
            result.append(specie.id)
    return result

# Count herpetofauna rescue by family


async def count_herpetofauna_rescue_by_family(
        db: AsyncSession,
        family_id: int
        ) -> int:
    if not family_id:
        return 0
    stmt = select(
            func.count(RescueHerpetofauna.id)
            ).where(
                    RescueHerpetofauna.family_id == family_id
                    )

    result = await db.execute(stmt)

    total= result.scalar()

    if total is None:
        return 0

    return total

#count mammal rescue by family
async def count_mammal_rescue_by_family(db: AsyncSession, family_id:int) -> int :
    if not family_id:
        return 0
    stmt = select(func.count(RescueMammals.id)).where(RescueMammals.family_id == family_id)

    result = await db.execute(stmt)

    total= result.scalar()

    if total is None:
        return 0

    return total 


# Get class_ id and class_ name by specie id
async def get_class_id_and_name_by_specie_id(
        db: AsyncSession,
        specie_id: int
        ) -> Class_ | HTTPException:
    specie = await get_specie_by_id(db, specie_id)
    if not specie:
        return HTTPException(status_code=404, detail="Specie not found")
    genus = await get_genus_by_id(db, specie.genus_id)
    if not genus:
        return HTTPException(status_code=404, detail="Genus not found")
    family = await get_family_by_id(db, genus.family_id)
    if not family:
        return HTTPException(status_code=404, detail="Family not found")
    order = await get_order_by_id(db, family.order_id)
    if not order:
        return HTTPException(status_code=404, detail="Order not found")
    class_ = await get_class_by_id(db, order.class__id)
    if not class_:
        return HTTPException(status_code=404, detail="Class not found")
    return class_









