from sqlalchemy.orm import Session
from typing import List, Union
from fastapi import HTTPException

from app.schemas.species import Species, SpeciesCreate, Genuses, GenusesCreate, Families, FamiliesCreate, Orders, OrdersCreate, Classes, ClassesCreate
from app.models.species import Specie, Genus, Family, Order, Class_

#Purpose: CRUD operations for Species

#Get if specie exists
async def get_specie_by_name(db: Session, scientific_name: str) -> Union[Specie, None]:
    return db.query(Specie).filter(Specie.scientific_name == scientific_name).first()

#Create a specie
async def create_specie(db: Session, specie: SpeciesCreate) -> Specie:
    db_specie = Specie(
        scientific_name = specie.scientific_name,
        common_name = specie.common_name,
        genus_id = specie.genus_id
    )
    db.add(db_specie)
    db.commit()
    db.refresh(db_specie)
    return db_specie

#Get all species
async def get_all_species(db: Session) -> List[Specie]:
    return db.query(Specie).all()

#Get specie by id
async def get_specie_by_id(db: Session, specie_id: int) -> Union[Specie, None]:
    return db.query(Specie).filter(Specie.id == specie_id).first()

#Update specie
async def update_specie(db: Session, specie_id: int, specie: SpeciesCreate) -> Specie:
    db_specie = db.query(Specie).filter(Specie.id == specie_id).first()
    if not db_specie:
        raise HTTPException(status_code=404, detail="Specie not found")
    db_specie.scientific_name = specie.scientific_name
    db_specie.common_name = specie.common_name
    db_specie.genus_id = specie.genus_id
    db.commit()
    db.refresh(db_specie)
    return db_specie

#Delete specie
async def delete_specie(db: Session, specie_id: int) -> Specie:
    db_specie = db.query(Specie).filter(Specie.id == specie_id).first()
    if not db_specie:
        raise HTTPException(status_code=404, detail="Specie not found")
    db.delete(db_specie)
    db.commit()
    return db_specie

#Create a genus
async def create_genus(db: Session, genus: GenusesCreate) -> Genus:
    db_genus = Genus(
        genus_name = genus.genus_name,
        family_id = genus.family_id
    )
    db.add(db_genus)
    db.commit()
    db.refresh(db_genus)
    return db_genus 

#Get all genuses
async def get_all_genuses(db: Session) -> List[Genus]:
    return db.query(Genus).all()

#Get genus by id
async def get_genus_by_id(db: Session, genus_id: int) -> Union[Genus, None]:
    return db.query(Genus).filter(Genus.id == genus_id).first()

#Get genus by name
async def get_genus_by_name(db: Session, genus_name: str) -> Union[Genus, None]:
    return db.query(Genus).filter(Genus.genus_name == genus_name).first()

#Update genus
async def update_genus(db: Session, genus_id: int, genus: GenusesCreate) -> Genus:
    db_genus = db.query(Genus).filter(Genus.id == genus_id).first()
    if not db_genus:
        raise HTTPException(status_code=404, detail="Genus not found")
    db_genus.genus_name = genus.genus_name
    db_genus.family_id = genus.family_id
    db.commit()
    db.refresh(db_genus)
    return db_genus

#Delete genus
async def delete_genus(db: Session, genus_id: int) -> Genus:
    db_genus = db.query(Genus).filter(Genus.id == genus_id).first()
    if not db_genus:
        raise HTTPException(status_code=404, detail="Genus not found")
    db.delete(db_genus)
    db.commit()
    return db_genus

#Create a family
async def create_family(db: Session, family: FamiliesCreate) -> Family:
    db_family = Family(
        family_name = family.family_name,
        order_id = family.order_id
    )
    db.add(db_family)
    db.commit()
    db.refresh(db_family)
    return db_family    

#Get all families
async def get_all_families(db: Session) -> List[Family]:
    return db.query(Family).all()

#Get family by id
async def get_family_by_id(db: Session, family_id: int) -> Union[Family, None]:
    return db.query(Family).filter(Family.id == family_id).first()

#Get family by name
async def get_family_by_name(db: Session, family_name: str) -> Union[Family, None]:
    return db.query(Family).filter(Family.family_name == family_name).first()

#Update family
async def update_family(db: Session, family_id: int, family: FamiliesCreate) -> Family:
    db_family = db.query(Family).filter(Family.id == family_id).first()
    if not db_family:
        raise HTTPException(status_code=404, detail="Family not found")
    db_family.family_name = family.family_name
    db_family.order_id = family.order_id
    db.commit()
    db.refresh(db_family)
    return db_family

#Delete family
async def delete_family(db: Session, family_id: int) -> Family:
    db_family = db.query(Family).filter(Family.id == family_id).first()
    if not db_family:
        raise HTTPException(status_code=404, detail="Family not found")
    db.delete(db_family)
    db.commit()
    return db_family

#Create an order
async def create_order(db: Session, order: OrdersCreate) -> Order:
    db_order = Order(
        order_name = order.order_name,
        class__id = order.class__id
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

#Get all orders
async def get_all_orders(db: Session) -> List[Order]:
    return db.query(Order).all()

#Get order by id
async def get_order_by_id(db: Session, order_id: int) -> Union[Order, None]:
    return db.query(Order).filter(Order.id == order_id).first()

#Get order by name
async def get_order_by_name(db: Session, order_name: str) -> Union[Order, None]:
    return db.query(Order).filter(Order.order_name == order_name).first()

#Update order
async def update_order(db: Session, order_id: int, order: OrdersCreate) -> Order:
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db_order.order_name = order.order_name
    db_order.class__id = order.class__id
    db.commit()
    db.refresh(db_order)
    return db_order

#Delete order
async def delete_order(db: Session, order_id: int) -> Order:
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(db_order)
    db.commit()
    return db_order

#Create a class
async def create_class(db: Session, class_: ClassesCreate) -> Class_:
    db_class = Class_(
        class_name = class_.class_name,
    )
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class

#Get all classes    
async def get_all_classes(db: Session) -> List[Class_]:
    return db.query(Class_).all()

#Get class by id
async def get_class_by_id(db: Session, class_id: int) -> Union[Class_, None]:
    return db.query(Class_).filter(Class_.id == class_id).first()

#Get class by name
async def get_class_by_name(db: Session, class_name: str) -> Union[Class_, None]:
    return db.query(Class_).filter(Class_.class_name == class_name).first()

#Update class
async def update_class(db: Session, class_id: int, class_: ClassesCreate) -> Class_:
    db_class = db.query(Class_).filter(Class_.id == class_id).first()
    if not db_class:
        raise HTTPException(status_code=404, detail="Class not found")
    db_class.class_name = class_.class_name
    db.commit()
    db.refresh(db_class)
    return db_class

#Delete class
async def delete_class(db: Session, class_id: int) -> Class_:
    db_class = db.query(Class_).filter(Class_.id == class_id).first()
    if not db_class:
        raise HTTPException(status_code=404, detail="Class not found")
    db.delete(db_class)
    db.commit()
    return db_class




