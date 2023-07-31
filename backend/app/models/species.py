from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

import app.db.database as _database
import app.models.images

class Specie(_database.Base):
    __tablename__:str = "species"
    id: Column = Column(Integer, primary_key=True, index=True)
    scientific_name: Column = Column(String, unique=True, index=True)
    specific_epithet: Column = Column(String, index=True)
    create_at: Column[datetime] = Column(DateTime, default=datetime.utcnow)
    # Relationships
    genus_id: Column = Column(Integer, ForeignKey("genus.id"))
    genus = relationship("Genus", back_populates="species")

    # Relationships with flora_rescue
    flora_rescue_bryophyte = relationship("FloraRescue", back_populates="specie_bryophyte", foreign_keys="FloraRescue.specie_bryophyte_id")
    flora_rescue_epiphyte = relationship("FloraRescue", back_populates="specie_epiphyte", foreign_keys="FloraRescue.specie_epiphyte_id")

    # Relationships with plant_nursery
    plant_nursery = relationship("PlantNursery", back_populates="specie")

    # Relationships with flora_relocation
    flora_relocation_bryophyte = relationship("FloraRelocation", back_populates="specie_bryophyte")

    # Relationships with images
    images = relationship("Image", back_populates="species")


class Genus(_database.Base):
    __tablename__:str = "genus"
    id: Column = Column(Integer, primary_key=True, index=True)
    genus_name: Column = Column(String, unique=True, index=True)
    genus_full_name: Column = Column(String, unique=True, index=True, nullable=True)
    create_at: Column[datetime] = Column(DateTime, default=datetime.utcnow)

    # Relationships specie and family
    family_id: Column = Column(Integer, ForeignKey("family.id"))
    family = relationship("Family", back_populates="genus")
    species = relationship("Specie", back_populates="genus")

    # Relationships with flora_rescue
    flora_rescue_bryophyte = relationship("FloraRescue", back_populates="genus_bryophyte", foreign_keys="FloraRescue.genus_bryophyte_id")



class Family(_database.Base):
    __tablename__:str = "family"
    id: Column = Column(Integer, primary_key=True, index=True)
    family_name: Column = Column(String, unique=True, index=True)
    create_at: Column[datetime] = Column(DateTime, default=datetime.utcnow)

    # Relationships order and genus
    order_id: Column = Column(Integer, ForeignKey("order.id"))
    order = relationship("Order", back_populates="family")
    genus = relationship("Genus", back_populates="family")

    # Relationships with flora_rescue
    flora_rescue_bryophyte = relationship("FloraRescue", back_populates="family_bryophyte", foreign_keys="FloraRescue.family_bryophyte_id")

class Order(_database.Base):
    __tablename__:str = "order"
    id: Column = Column(Integer, primary_key=True, index=True)
    order_name: Column = Column(String, unique=True, index=True)
    create_at: Column[datetime] = Column(DateTime, default=datetime.utcnow)

    # Relationships
    class__id: Column = Column(Integer, ForeignKey("class_.id"))
    class_ = relationship("Class_", back_populates="order")
    family = relationship("Family", back_populates="order")


class Class_(_database.Base):
    __tablename__:str = "class_"
    id: Column = Column(Integer, primary_key=True, index=True)
    class_name: Column = Column(String, unique=True, index=True)
    create_at: Column[datetime] = Column(DateTime, default=datetime.utcnow)

    # Relationships
    order = relationship("Order", back_populates="class_")
