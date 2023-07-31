import random
import string
from app.tests.conftest import *
from app.models.species import Specie, Genus, Family, Order, Class_


db: Session = next(override_get_db())

def create_specie_id() ->int:
    #query to get first Specie
    specie = db.query(Specie).first()
    # get id of the first specie
    if specie is not None:
        specie_id = specie.id
        return specie_id
    else:
        specie_id: int=random.randint(1, 1000)
        # Create a class
        db_class = Class_(
            id=777,
            class_name = "Mammalia",
        )
        db.add(db_class)
        db.commit()
        db.refresh(db_class)

        # Create an order
        db_order = Order(
            id=777,
            order_name = "Carnivora",
            class__id = db_class.id,
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)

        # Create a family
        db_family = Family(
            id=777,
            family_name = "Felidae",
            order_id = db_order.id,
        )
        db.add(db_family)
        db.commit()
        db.refresh(db_family)

        # Create a genus
        db_genus = Genus(
            id=777,
            genus_name = "Panthera",
            family_id = db_family.id,
        )
        db.add(db_genus)
        db.commit()
        db.refresh(db_genus)

        # Create a specie
        db_specie = Specie(
            id=specie_id,
            scientific_name = "Panthera leo",
            specific_epithet = "Leo",
            genus_id = db_genus.id,
        )
        db.add(db_specie)
        db.commit()
        db.refresh(db_specie)

        return specie_id

def create_genus_id() ->int:
    #query to get first Genus
    genus = db.query(Genus).first()
    # get id of the first genus
    if genus is not None:
        genus_id = genus.id
        return genus_id
    else:
        genus_id: int=random.randint(1, 1000)
        # Create a class
        db_class = Class_(
            id=778,
            class_name = "Mammalia2",
        )
        db.add(db_class)
        db.commit()
        db.refresh(db_class)

        # Create an order
        db_order = Order(
            id=778,
            order_name = "Carnivora2",
            class__id = db_class.id,
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)

        # Create a family
        db_family = Family(
            id=778,
            family_name = "Felidae2",
            order_id = db_order.id,
        )
        db.add(db_family)
        db.commit()
        db.refresh(db_family)

        # Create a genus
        db_genus = Genus(
            id=genus_id,
            genus_name = "Panthera2",
            family_id = db_family.id,
        )
        db.add(db_genus)
        db.commit()
        db.refresh(db_genus)

        return genus_id

def create_family_id() ->int:
    #query to get first Family
    family = db.query(Family).first()
    # get id of the first family
    if family is not None:
        family_id = family.id
        return family_id
    else:
        family_id: int=random.randint(1, 1000)
        # Create a class
        db_class = Class_(
            id=779,
            class_name = "Mammalia3",
        )
        db.add(db_class)
        db.commit()
        db.refresh(db_class)

        # Create an order
        db_order = Order(
            id=779,
            order_name = "Carnivora3",
            class__id = db_class.id,
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)

        # Create a family
        db_family = Family(
            id=family_id,
            family_name = "Felidae3",
            order_id = db_order.id,
        )
        db.add(db_family)
        db.commit()
        db.refresh(db_family)

        return family_id

#make a fuction that return a random string of 10 characters
def random_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=10))



#make a fuction that return a random int between 1 and 1000
def random_int() -> int:
    return random.randint(1,1000)

